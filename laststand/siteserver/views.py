# necessary Django imports to run the websites
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.utils.encoding import smart_str
from .models import PublisherUsers, Articles
from django.contrib.auth.decorators import login_required


# other imports that are useful
import helpers as h
import datetime as dt
import json as j


# Basic page display views
def index(request):
    request.session["offset"] = 0
    return h.return_as_wanted(request, "home.html")


def rates(request):
    return h.return_as_wanted(request, "rates.html")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        return render(request, "login.html")


def register_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        return render(request, "signup.html")

@login_required
def publish_page(request):
    # display not found error if they are anonymous user
    if not request.user.is_authenticated:
        return HttpResponseNotFound(render(request, "error.html"))

    # take them to a home page if they are signed in, but not a publisher
    user = PublisherUsers.objects.filter(base_user=request.user.id)
    if not user:
        return redirect("/")
    else:
        return h.return_as_wanted(request, "publish.html")

@login_required
def issue_page(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound(render(request, "error.html"))
    return h.return_as_wanted(request, "issue.html")

def account_page(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound(render(request, "error.html"))
    return h.return_as_wanted(request, "account_page.html", message={"username": request.user.get_username(), "date_joined": request.user.date_joined })


def downloads(request):
    if not request.user.is_authenticated:
        return h.return_as_wanted(request, "login.html", message=["warning", "You must sign in or sign up to download the cloud"])
    else:
        return h.return_as_wanted(request, "download.html")

# either just log out user, or take them to login to switch to another account
def relog_page(request):
    logout(request)
    return redirect("/login")


def logout_user(request):
    logout(request)
    return redirect("/")


def license_page(request):
    return h.return_as_wanted(request, "legal_docs.html")


def password_page(request):
    return h.return_as_wanted(request, "password-page.html")


# form submission pages for either a login. registration, or an article(publishers only)
@require_http_methods(["POST"])
def submit_login(request):
    username = request.POST["user"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return redirect("/")
    else:
        return h.return_as_wanted(request, "login.html", message=["danger", " Username and password combo does not exist!"])


@require_http_methods(["POST"])
def submit_register(request):
    email = request.POST["email"]
    username = request.POST["user"]
    password = h.sha256_hash(request.POST["password"])

    if not authenticate(request, username=username, password=password):
        user = User.objects.create_user(username, email, password)
        user.save()
        login(request, user)
        return redirect("/more-info")
    else:
        return h.return_as_wanted(request, "register", message=["Error!", "Username or email is already registered!"])


@require_http_methods(["POST"])
def submit_article(request):

        title = request.POST["title"]
        credit = request.POST["credit"]

        # use this to make sure a file was sent
        file = request.FILES
        content = request.POST["content"]

        if "file" in file.keys():
            # if it was, now make the 'file' variable into the actual file
            file = file["file"]

            # for any image, they have to at least leave some author credit
            if not len(credit) > 1:
                return h.return_as_wanted(request, "publish.html", message=["danger", "Your article was not accepted, you need to"
                                                                                    " supply an author credit to your image"])
            if "<self>" not in credit or "<logo>" not in credit:
                credit = "Photo courtesy of " + credit
            elif "<self>" in credit:
                credit = credit.replace("<self>", "")

            # write the file to the article_images static directory. WAAAY easier than the Flask version
            with open( "./static/article_images/" + file.name, "wb+") as f:
                for chunk in file.chunks():
                    f.write(chunk)

            # give the user a success message, and save their article
            new_article = Articles.objects.create(title=title, author=request.user.get_full_name(), image_title=credit,
                                                  date=dt.datetime.now().strftime("%m/%d/%y"), image_src=file.name, text=content)
            new_article.save()
            return h.return_as_wanted(request, "publish.html", message=["success", "Your article was published successfully!"])

        else:
            # publishers don't have to put an image in their article
            new_article = Articles.objects.create(date=dt.datetime.now().strftime("%m/%d/%y"), author=request.user.get_full_name(),
                                                  title=title, text=content)
            new_article.save()

            return h.return_as_wanted(request, "publish.html",
                                    message=["success", "Your article was published successfully!"])

@require_http_methods(["POST"])
def submit_issue(request):
    name = request.POST["your-name"]
    email = request.POST["your-email"]
    issue_type = request.POST["issue"]
    issue = request.POST["issue-text"]

    try:
        success = send_mail(issue_type, name + " -\n" + issue, email, ["vtrolia@live.com"])
    except BadHeaderError:
        return h.return_as_wanted(request, "issue.html", ["danger", "Your email was unable to be sent!"])

    if success < 1:
        return h.return_as_wanted(request, "issue.html", ["danger"], "Something went wrong, your email was not sent!")
    else:
        return h.return_as_wanted(request, "issue.html", ["success", "Your message was successfully delivered!"])


def submit_download(request):
    # either send them back the full software suite or just the client
    if "both" in request.POST:
        response_name = "LaststandCLI.zip"
    else:
        response_name = "laststand_client.zip"

    # read the file as the contents of the message
    with open("./static/downloads/" + request.POST["os-type"] + "/" + response_name, "rb") as f:
        response = HttpResponse(f.read())

    # these headers are needed so that the client understands the file being sent to them
    response["Content-Disposition"] = "attachment; filename='" + response_name +"'"
    response["X-Sendfile"] = smart_str("./static/downloads/" + request.POST["os-type"] + "/" + response_name)
    return response

@require_http_methods(["POST"])
def submit_password_change(request):
    old, new = request.body.decode("utf-8").split("&")
    if authenticate(request, username=request.user.get_username(), password=old):
        request.user.set_password(new)
        request.user.save()
        return HttpResponse("<div class=\"alert alert-success\" role=\"alert\" id=\"alerts\"><strong>Success!</strong> " +
                            " Your password was successfully changed!</div>")
    else:
        return HttpResponse("<div class=\"alert alert-danger\" role=\"alert\" id=\"alerts\"><strong>Error! </strong>" +
                            " Your old password was not correct!</div>")


@require_http_methods(["POST"])
def submit_delete_account(request):
    password = request.POST['password']

    if authenticate(request, username=request.user.get_username(), password=password):
        request.user.delete()
        logout(request)
        return h.return_as_wanted(request, "login.html", message=["warning", " Your account has successfully been deleted!"])
    else:
        return redirect("/")


def submit_application(request):
    file = request.FILES['example']

    mail = EmailMessage(request.user.get_username() + " wants to become a Publisher!",
                        "This is what they had to say:\n\n" + request.POST['introduction'],
                        "laststandnoreply@protonmail.com",
                        ["laststand@protonmail.com"])
    mail.attach(file.name, file.read(), "application/octet-stream")
    mail.send()
    return redirect("/account-settings")



# other forms or requests to send data
def more_info(request):
    if not request.user.is_authenticated:
        return redirect("/")
    else:
        return h.return_as_wanted(request, "user_details.html")


@require_http_methods(["POST"])
def add_name(request):
    first = request.POST["firstName"]
    last = request.POST["lastName"]

    # let users add their first and last name, or skip it if they don't
    user = User.objects.get(username=request.user.get_username())
    user.first_name = first
    user.last_name = last
    user.save()
    return redirect("/")


@require_http_methods(["POST"])
def story(request):
    with open("./siteserver/templates/ourstory.html") as f:
        content = f.read()
    return HttpResponse(content)


def load_articles(request):
    # keep track of the articles that have been loaded so far, so that it isn't grabbing more and more forever
    if not "offset" in request.session.keys():
        request.session["offset"] = 0

    # get them in reverse order, then make all of the objects into one big JSON object, using "i" as the key for each
    article = Articles.objects.order_by("-id")[request.session["offset"]: request.session["offset"] + 5]
    articles = {}
    request.session["offset"] += 5
    i = 0
    for art in article:
        articles[str(i)] = art.asJSON()
        i += 1

    # an empty response leads to the story being loaded, so send nothing back if there are no more articles left
    if not articles:
        return HttpResponse("")
    return HttpResponse(j.dumps(articles))


def load_cloud_options(request):
    return render(request, "cloud-placeholder.html")


def load_base_options(request):
    return render(request, "base_settings_page.html")


def load_change_plan(request):
    return render(request, "cloud-placeholder.html")

def load_delete_page(request):
    return render(request, "delete.html")

def load_request_publisher(request):
    if request.user.first_name:
        return render(request, "become_publisher.html", context={"font_size": "1em", "name": request.user.first_name})
    else:
        return render(request, "become_publisher.html", context={"font_size": ".91em"})


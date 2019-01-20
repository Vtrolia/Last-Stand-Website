# necessary Django imports to run the websites
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from siteserver.models import PublisherUsers, Articles

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


def publish_page(request):
    # display not found error if they are anonymous user
    if not request.user.is_authenticated:
        return HttpResponseNotFound(render(request, "error.html"))

    # take them to a home page if they are signed in, but not a publisher
    user = PublisherUsers.objects.filter(base_user=request.user.id)
    """if not user:
        return redirect("/")
    else:"""
    return h.return_as_wanted(request, "publish.html")


# either just log out user, or take them to login to switch to another account
def relog_page(request):
    logout(request)
    return redirect("/login")


def logout_user(request):
    logout(request)
    return redirect("/")


# form submission pages for either a login. registration, or an article(publishers only)
@require_http_methods(["POST"])
def submit_login(request):
    username = request.POST["user"]
    password = h.sha256_hash(request.POST["password"])
    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return redirect("/")
    else:
        return h.return_as_wanted(request, "login.html", message=["ERROR!", " Username and password combo does not exist!"])


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

            # write the file to the article_images static directory. WAAAY easier than the Flask version
            with open( "./static/article_images" + file.name, "wb+") as f:
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
    if not "offset" in request.session.keys():
        request.session["offset"] = 0

    article = Articles.objects.order_by("-id")[request.session["offset"]: request.session["offset"] + 5]
    articles = {}
    request.session["offset"] += 5
    i = 0
    for art in article:
        articles[str(i)] = art.asJSON()
        i += 1

    if not articles:
        return HttpResponse("")
    return HttpResponse(j.dumps(articles))


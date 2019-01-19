from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
import hashlib as h


# Create your views here.
def index(request):
    return return_as_wanted(request, "home.html")


def rates(request):
    return return_as_wanted(request, "rates.html")


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


def logout_user(request):
    logout(request)
    return return_as_wanted(request, "home.html")


@require_http_methods(["POST"])
def submit_login(request):
    username = request.POST["user"]
    password = sha256_hash(request.POST["password"])
    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return return_as_wanted(request, "home.html")
    else:
        return return_as_wanted(request, "login.html", message=["ERROR!", " Username and password combo does not exist!"])


@require_http_methods(["POST"])
def submit_register(request):
    email = request.POST["email"]
    username = request.POST["user"]
    password = sha256_hash(request.POST["password"])

    if not authenticate(request, username=username, password=password):
        user = User.objects.create_user(username, email, password)
        user.save()
        login(request, user)
        return redirect("/more-info")
    else:
        return return_as_wanted(request, "register", message=["Error!", "Username or email is already registered!"])


def more_info(request):
    if not request.user.is_authenticated:
        return redirect("/")
    else:
        return return_as_wanted(request, "user_details.html")


@require_http_methods(["POST"])
def add_name(request):
    first = request.POST["firstName"]
    last = request.POST["lastName"]

    user = User.objects.get(username=request.user.get_username())
    user.first_name = first
    user.last_name = last
    user.save()
    return redirect("/")


# not a view, this function is a helper so that the user can constantly be assured that they are still logged in
def return_as_wanted(request, template, message=None):
    if request.user.is_authenticated:
        if request.user.get_short_name():
            try:
                if len(request.user.get_short_name()) > 14:
                    name = request.user.get_short_name()[:11] + "..."
                else:
                    name = request.user.get_short_name()
            except:
                pass
            return render(request, template, context={"name": "Welcome Back, " + str(name) + "!",
                                             "message": message})

        if len(request.user.get_username()) > 14:
            greeting = request.user.get_username()[:11] + "..."
        else:
            greeting = request.user.get_username()
        return render(request, template, context={"name": "Welcome Back, " + str(greeting) + "!", "message": message})

    return render(request, template, context={"message": message})


# helper function to more neatly create the SHA256 hash of the password. I know Django says that they have encryption
# built into their password validation, but I was able to see the plaintext password when I looked at the user object
def sha256_hash(password):
    return h.sha256(password.encode()).hexdigest()

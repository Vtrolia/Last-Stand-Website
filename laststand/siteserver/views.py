from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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
            return render(template, context={"name": "Welcome Back, " + str(name) + "!",
                                             "message": message})

        if len(request.user.get_username()) > 14:
            greeting = request.user.get_username()[:11] + "..."
        else:
            greeting = request.user.get_username()
        return render(request, template, context={"name": "Welcome Back, " + str(greeting) + "!", "message": message})

    return render(request, template)


# helper function to more neatly create the SHA256 hash of the password
def sha256_hash(password):
    return h.sha256(password.encode()).hexdigest()

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout


# Create your views here.
from django.views.decorators.http import require_http_methods


def home(request):
    if request.user.is_authenticated:
        return render(request, "index.html", context={"name": request.user})
    return render(request, "index.html")


def ocsp(request):
    if request.user.is_authenticated:
        return render(request, "ocsp.html", context={"name": request.user})
    return render(request, "ocsp.html")


def statuses(request):
    if request.user.is_authenticated:
        return render(request, "account.html", context={"name": request.user})
    return render(request, "account.html")


def login_user(request):
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("/")


@require_http_methods(["POST"])
def submit_login(request):
    user = User.objects.get(username=request.POST['username'])
    if not user:
        user = User.objects.create_user(request.POST['username'], None, request.POST['password'])
        user.save()
    else:
        user.set_password(request.POST['password'])
        user.save()
    login(request, user)
    return redirect("/")


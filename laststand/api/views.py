from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import Cloud
from django.contrib.auth.models import User

import helpers as h
import requests


# Create your views here.
def index(request):
    pass


@csrf_exempt
def set_info(request, id):
    user, password = request.META["QUERY_STRING"].split("&")
    user = user.split("=")[1]
    password = password.split("=")[1]

    owner = authenticate(request, username="Vinny", password="ShitBag1")

    if owner == Cloud.objects.get(id=id).owner:
        cloud = Cloud.objects.get(id=id)
        content = ""
        for user in cloud.users.all():
            content += user.username + " " + user.password + "\n"
        return HttpResponse("stfoo mga")
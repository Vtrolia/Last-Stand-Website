from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import Cloud

import helpers as h


# Create your views here.
def index(request):
    pass


@csrf_exempt
def set_info(request, id):
    user, password = request.META["QUERY_STRING"].split("&")
    user = user.split("=")[1]
    password = password.split("=")[1]

    owner = authenticate(request, username=user, password=password)

    if owner == Cloud.objects.get(id=id).owner:
        cloud = Cloud.objects.get(id=id)
        cloud.ip_address = request.META["HTTP_HOST"]
        cloud.save()
        content = ""
        for user in cloud.users.all():
            content += "content: " + user.username + " " + user.password + "\r\n"
        return HttpResponse(content)
    else:
        return HttpResponse("contents: none failure" + "\r\n")


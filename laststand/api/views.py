from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Cloud, SSL

import helpers as h
import datetime as dt

# Create your views here.
def index(request):
    pass


@csrf_exempt
@require_http_methods(["POST"])
def set_info(request, name):
    owner = h.api_user_check(request)

    # if the owner is not the correct one, something is wrong, and nothing will be updated for security reasons
    if owner == Cloud.objects.get(id=name).owner:
        cloud = Cloud.objects.get(id=name)
        cloud.ip_address = request.META["HTTP_HOST"]

        # while updating, if the ssl certificate is now expired, delete it. 
        if dt.datetime.now() >= cloud.ssl_cert.date_expires:
            cloud.ssl_cert.delete()

        cloud.save()
        content = ""

        # formatting the credentials like this made it easy to parse on the cloud end
        for user in cloud.users.all():
            content += "content: " + user.username + " " + user.password + "\r\n"
        return HttpResponse(content)
    else:
        return HttpResponse("contents: none failure" + "\r\n")



@csrf_exempt
@require_http_methods(["POST"])
def get_address(request, name):
    accessor = h.api_user_check(request)

    if accessor:
        resp = HttpResponse("content: " + Cloud.objects.get(id=name).ip_address + "\r\n")
    else:
        resp = HttpResponse("content: \r\n")

    return resp


@csrf_exempt
def get_ssl_cert(request, name):
    cert = Cloud.objects.get(id=name).ssl_cert
    if cert.date_expires > dt.datetime.now():
        return HttpResponse(cert.cacert)
    else:
        cert.delete()
        return HttpResponse("")





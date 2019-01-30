from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Cloud, SSL

import helpers as h
from dateutil.relativedelta import relativedelta
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

@csrf_exempt
@require_http_methods(["POST"])
def renew_cert(request, name):
    owner = h.api_user_check(request)

    if owner:
        cert = Cloud.objects.get(id=name)
        privkey = cert.ssl_cert.privkey
        print(h.generate_new_cert(ownername=owner.username, ownerpass=owner.password, name=name, privkey=privkey))
    else:
        return HttpResponse("")


@require_http_methods(["POST"])
def submit_cloud(request):
    created = dt.datetime.now()
    expires = created + relativedelta(month = 6)
    if not request.user.is_authenticated:
        return HttpResponse("")
    else:
        owner = request.user
        name = h.troliAlgoritm(owner.username, owner.password)
        auth_info = h.generate_new_cert(owner.username, owner.password, name)
        print(auth_info)
        ssl = SSL.objects.create(cacert=auth_info[0], privkey=auth_info[1], date_created=created, date_expires=expires,
                                 created_by=owner, owned_by=owner)
        ssl.save()
        given_name = request.POST['name']
        ip_address = request.POST['ip']
        status = 0
        cloud = Cloud.objects.create(id=name, name=given_name, ip_address=ip_address, ssl_cert=ssl, users=[owner],
                                     owner=owner, status=0)
        cloud.save()
        return HttpResponse(auth_info)
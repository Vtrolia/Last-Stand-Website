from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Cloud, SSL

import helpers as h
from dateutil.relativedelta import relativedelta
import datetime as dt
import json as j

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
        if dt.date.today() >= cloud.ssl_cert.date_expires:
            cloud.ssl_cert.delete()

        cloud.save()
        content = ""

        # formatting the credentials like this made it easy to parse on the cloud end
        for user in cloud.users.all():
            content += "content: " + user.username + " " + user.password + "\r\n"
        return HttpResponse(content)
    else:
        return HttpResponse("contents: none failure" + "\r\n")


@require_http_methods(["POST"])
def get_user_info(request):
    if not request.user.is_authenticated:
        return HttpResponse("")
    else:
        response = dict()

        response["status"] = "Basic"

        clouds = Cloud.objects.filter(owner=request.user)
        response["clouds_owned"] = clouds.count()
        response["clouds"] = []

        if not clouds.count():
            response["clouds"] = ["You haven't created a Cloud yet!"]
            return HttpResponse(j.dumps(response))

        for cloud in clouds:
            response['clouds'].append(cloud.name)

        return HttpResponse(j.dumps(response))





@csrf_exempt
@require_http_methods(["POST"])
def get_address(request, name):
    resp = HttpResponse("content: " + Cloud.objects.get(id=name).ip_address + "\r\n")
    return resp


@csrf_exempt
def get_ssl_cert(request, name):
    # anyone can get the certificate for a server, just not the private key or any other data
    cert = Cloud.objects.get(id=name).ssl_cert

    # delete an invalid cert
    if cert.date_expires > dt.date.today():
        return HttpResponse(cert.cacert)
    else:
        cert.delete()
        return HttpResponse("")


@csrf_exempt
def is_cert_valid(request, name):
    # anyone can check whether or not a server has a valid ssl certificate or not
    cert = Cloud.objects.get(id=name).ssl_cert
    if cert.date_expires <= dt.date.today():
        cert.delete()
        return HttpResponse("content: expired")
    else:
        return HttpResponse("content: valid")


@csrf_exempt
@require_http_methods(["POST"])
def renew_cert(request, name):
    owner = h.api_user_check(request)

    # only the owner is allowed to make a request for a new ssl certificate
    if owner:
        cert = Cloud.objects.get(id=name).ssl_cert

        # create a completely new cert w/o deleting
        new_cert = h.generate_new_cert(ownername=owner.username, ownerpass=owner.password, name=name)
        cert.cacert = new_cert[0]
        cert.privkey = new_cert[1]
        cert.date_created = dt.datetime.now()
        cert.date_expires = dt.datetime.now() + relativedelta(month=6)
        cert.save()
        return HttpResponse(new_cert)
    else:
        return HttpResponse("")


@require_http_methods(["POST"])
def submit_cloud(request):
    # this is the initial creation of a cloud, so set the date
    created = dt.datetime.now()
    expires = created + relativedelta(month = 6)
    if not request.user.is_authenticated:
        return HttpResponse("")
    else:

        # has to be an authenticated user to create a cloud
        owner = request.user

        # first create the ssl cert
        name = h.troliAlgorithm(owner.username, owner.password)
        auth_info = h.generate_new_cert(owner.username, owner.password, name)
        ssl = SSL.objects.create(cacert=auth_info[0], privkey=auth_info[1], date_created=created, date_expires=expires,
                                 created_by=owner, owned_by=owner)
        ssl.save()

        # once the cert is saved, now connect it to the cloud being created. The user can give it a custom name, but
        # its id is generated
        given_name = request.POST['name']
        ip_address = request.POST['ip']
        cloud = Cloud.objects.create(id=name, name=given_name, ip_address=ip_address, ssl_cert=ssl, owner=owner, status=0)
        cloud.save()
        return HttpResponse(auth_info)

@csrf_protect
def verify(request):
    users = User.objects.all()
    usernames = {"username": [], "email": []}

    for user in users:
        usernames["username"].append(user.username)
        usernames["email"].append(user.email)

    return HttpResponse(j.dumps(usernames))
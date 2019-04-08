# django imports
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.encoding import smart_str

# import api models
from .models import Cloud, SSL

# regular imports
from dateutil.relativedelta import relativedelta
import datetime as dt
import helpers as h
import json as j
import os
import zipfile as zip


# Create your views here.
def index(request):
    pass

# this is where a cloud updates its own information stored on the website's databases
@csrf_exempt
def set_info(request, name):
    owner = h.api_user_check(request)

    # if the owner is not the correct one, something is wrong, and nothing will be updated for security reasons
    if owner == Cloud.objects.get(id=name).owner:
        cloud = Cloud.objects.get(id=name)
        cloud.ip_address = request.META["QUERY_STRING"].split("&")[2][3:]

        # while updating, if the ssl certificate is now expired, delete it.
        if dt.date.today() >= cloud.ssl_cert.date_expires:
            cloud.ssl_cert.delete()

        cloud.save()
        content = ""

        # formatting the credentials like this made it easy to parse on the cloud end
        for user in cloud.users.all():
            content += "content: " + user.username + " " + user.password.split("$")[2] + "\r\n"
        return HttpResponse(content)
    else:
        return HttpResponse("contents: none failure" + "\r\n")


# api getters
@csrf_exempt
def get_address(request, name):
    resp = HttpResponse("content: " + Cloud.objects.get(id=name).ip_address + "\r\n")
    return resp


@csrf_exempt
def get_ssl_cert(request, name):
    # anyone can get the certificate for a server, just not the private key or any other data
    cert = Cloud.objects.get(id=name).ssl_cert

    # delete an invalid cert
    if cert.date_expires > dt.date.today():
        cleaned_cert = "".join(cert.cacert.split('\r'))
        return HttpResponse("content: " + cleaned_cert)
    else:
        cert.delete()
        return HttpResponse("content: none")

def get_user_clouds(request):
    if not request.user.is_authenticated:
        return HttpResponse({"none", "failure"})
    else:
        clouds = Cloud.objects.filter(owner=request.user)
        
        cl = {}
        for cloud in clouds:
            cl[cloud.name] = cloud.name
        return HttpResponse(j.dumps(cl))


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
    
    
@csrf_protect
def verify(request):
    users = User.objects.all()
    usernames = {"username": [], "email": []}

    for user in users:
        usernames["username"].append(user.username)
        usernames["email"].append(user.email)

    return HttpResponse(j.dumps(usernames))
        
    
# certification validation and renewal    
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
        return HttpResponse(new_cert[0])
    else:
        return HttpResponse("")

    
# Views for creating/deleting clouds

# if the user wants to delete a cloud. verify who they are, then send them a message based on success or not 
@require_http_methods(["POST"])
def delete_cloud(request):
    req = j.loads(request.body.decode("utf-8"))
    if request.user.check_password(req['password']):
        cloud = Cloud.objects.get(owner=request.user, name=req['name'])
        ssl = cloud.ssl_cert
        cloud.delete()
        ssl.delete()
        
        resp = {
            "flag": "success",
            "body": "<strong>Success!</strong> Your cloud has been deleted!" 
            
        }
        return HttpResponse(j.dumps(resp))
    else:
        resp = {
            "flag": "danger",
            "body": "<strong>Error</strong> Something went wrong!"
        }
        return HttpResponse(j.dumps(resp))

    
# much like when submitting a cloud, when the user wants to download a client only for a cloud
# this view crafts a zip file with everything they need 
@require_http_methods(["POST"]) 
def download_client(request):
    name = request.POST['cloud-name']
    if request.POST['os-type'] == "none":
        return HttpResponse("Sorry, your Operating System is not supported yet")
    cloud = Cloud.objects.get(owner=request.user, name=name)
    
    # if the cloud created exists, send them the cloud id and client executable in the zip file
    if cloud:
        client_only = zip.ZipFile("/usr/local/www/Last-Stand-Website/laststand/laststandclient.zip", "w")
        with client_only.open("server_id", "w") as co:
            co.write(cloud.id.encode('utf-8'))
        
        with client_only.open("laststand", "w") as co:
            with open("/usr/local/www/Last-Stand-Website/laststand/static-folder/downloads/" +
                      request.POST["os-type"] + "/" + "laststand", "rb") as f:
                co.write(f.read())
        
        client_only.close()
        
        with open("/usr/local/www/Last-Stand-Website/laststand/laststandclient.zip", "rb") as f:
            response = HttpResponse(f.read())

        # these headers are needed so that the client understands the file being sent to them
        response["Content-Disposition"] = "attachment; filename=laststandclient.zip"
        response["X-Sendfile"] = smart_str("/usr/local/www/Last-Stand-Website/laststand/laststandclient.zip")
        os.remove("/usr/local/www/Last-Stand-Website/laststand/laststandclient.zip")
        return response


# when a user wants to create a new cloud, this view registers it, then sends them a download for this cloud
@require_http_methods(["POST"])
def submit_cloud(request):
    
    clouds = Cloud.objects.filter(owner=request.user)
    for cloud in clouds:
        if cloud.name == request.POST["name"]:
            return HttpResponse("Nice try, but setting the button back to active with inspect element is the easiest trick in the book, pick a new cloud name please")

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
        ip_address = request.META["REMOTE_ADDR"]
        cloud = Cloud.objects.create(id=name, name=given_name, ip_address=ip_address, ssl_cert=ssl, owner=owner, status=0)
        cloud.save()
    
        # now, the user is given a zip file containing what they need. Each of these files is stored on the server, so it is loaded
        # up and added to the zip archive
        archive = zip.ZipFile("/usr/local/www/Last-Stand-Website/laststand/laststand.zip", "w")
        with archive.open("Last Stand Cloud - End user License Agreement(EULA).pdf", "w") as ls:

            with open("/usr/local/www/Last-Stand-Website/laststand/static-folder/downloads/Last Stand Cloud - "
                      "End user License Agreement(EULA).pdf", "rb") as f:
                ls.write(f.read())

        # read the file as the contents of the message
        with archive.open("laststandserver", "w") as ls:

            with open("/usr/local/www/Last-Stand-Website/laststand/static-folder/downloads/" +
                      request.POST["os-type"] + "/laststandserver", "rb") as f:
                ls.write(f.read())

        with archive.open("laststand", "w") as ls:
            with open("/usr/local/www/Last-Stand-Website/laststand/static-folder/downloads/" +
                      request.POST["os-type"] + "/" + "laststand", "rb") as f:
                ls.write(f.read())

        with archive.open("cacert.pem", "w") as ls:
            ls.write(auth_info[0].encode('utf-8'))

        with archive.open("privkey.pem", "w") as ls:
            ls.write(auth_info[1].encode('utf-8'))

        with archive.open("server_id", "w") as ls:
            ls.write(cloud.id.encode('utf-8'))

        archive.close()

        with open("/usr/local/www/Last-Stand-Website/laststand/laststand.zip", "rb") as f:
            response = HttpResponse(f.read())

        # these headers are needed so that the client understands the file being sent to them
        response["Content-Disposition"] = "attachment; filename=laststand.zip"
        response["X-Sendfile"] = smart_str("/usr/local/www/Last-Stand-Website/laststand/laststand.zip")
        os.remove("/usr/local/www/Last-Stand-Website/laststand/laststand.zip")
        return response

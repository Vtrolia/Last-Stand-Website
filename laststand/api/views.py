# django imports
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.encoding import smart_str

# import api models
from .models import Cloud
from laststand.settings import HOME_DIR

# regular imports
from dateutil.relativedelta import relativedelta
import datetime as dt
import helpers as h
import json as j
import os
import tarfile as t


# Create your views here.
def index(request):
    pass


@csrf_exempt
def lsverify_login(request):
    req = j.loads(request.body)
    user = authenticate(request, username=req['username'], password=req['password'])
    if user:
        login(request, user)
        return HttpResponse("VALID")
    else:
        return HttpResponse("INVALID")

# this is where a cloud updates its own information stored on the website's databases
@csrf_exempt
def set_info(request, name):
    owner = h.api_user_check(request)

    # if the owner is not the correct one, something is wrong, and nothing will be updated for security reasons
    if owner == Cloud.objects.get(id=name).owner:
        cloud = Cloud.objects.get(id=name)
        cloud.ip_address = request.META["QUERY_STRING"].split("&")[2][3:]
        cloud.remote_address = request.META["REMOTE_ADDR"]

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


def get_user_clouds(request):
    if not request.user.is_authenticated:
        return HttpResponse({"none", "failure"})
    else:
        clouds = Cloud.objects.filter(owner=request.user)
        
        cl = {}
        for cloud in clouds:
            cl[cloud.name] = cloud.id
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
    
# Views for creating/deleting clouds

# if the user wants to delete a cloud. verify who they are, then send them a message based on success or not 
@require_http_methods(["POST"])
def delete_cloud(request):
    req = j.loads(request.body.decode("utf-8"))
    if request.user.check_password(req['password']):
        cloud = Cloud.objects.get(owner=request.user, name=req['name'])
        cloud.delete()
        
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

        # move to the downloads to craft the archive
        client_only = t.open(name=HOME_DIR + "Last-Stand-Website/laststand/static-folder/downloads/" + request.POST['os-type'] +
                                  "/laststandclient.tar.gz", mode="w:gz")
        old_dir = os.getcwd()
        os.chdir(HOME_DIR + "Last-Stand-Website/laststand/static-folder/downloads")

        # add files
        with open("server_id", "wb") as co:
            co.write(cloud.id.encode('utf-8'))
        client_only.add('server_id')
        os.remove("server_id")

        # close the archive and move back to the previous directory
        client_only.close()
        os.chdir(old_dir)

        with open(HOME_DIR + "/Last-Stand-Website/laststand/static-folder/downloads/" + request.POST['os-type'] + "/laststandclient.tar.gz", "rb") as f:
            response = HttpResponse(f.read())
        print("here")
        # these headers are needed so that the client understands the file being sent to them
        response["Content-Disposition"] = "attachment; filename=laststandclient.tar.gz"
        response["X-Sendfile"] = "laststandclient.tar.gz"
        return response
    else:
        return HttpResponse("Cloud was not found, sorry for the error")


# when a user wants to create a new cloud, this view registers it, then sends them a download for this cloud
@require_http_methods(["POST"])
def submit_cloud(request):
    
    clouds = Cloud.objects.filter(owner=request.user)
    for cloud in clouds:
        if cloud.name == request.POST["name"]:
            return HttpResponse("Nice try, but setting the button back to active with inspect element is the easiest "
                                "trick in the book, pick a new cloud name please")

    if not request.user.is_authenticated:
        return HttpResponse("")
    else:
        # has to be an authenticated user to create a cloud
        owner = request.user

        # first create the ssl cert
        name = h.troliAlgorithm(owner.username, owner.password)

        # once the cert is saved, now connect it to the cloud being created. The user can give it a custom name, but
        # its id is generated
        given_name = request.POST['name']
        ip_address = request.META["REMOTE_ADDR"]
        cloud = Cloud.objects.create(id=name, name=given_name, remote_address=ip_address, owner=owner, status=0)
        cloud.users.add(owner)
        cloud.save()

        with open(HOME_DIR + "/Last-Stand-Website/laststand/static-folder/downloads/" + request.POST["os-type"] + "/" +
                  request.POST['os-type'] + ".tar.gz", "rb") as f:
            response = HttpResponse(f.read())

        # these headers are needed so that the client understands the file being sent to them
        response["Content-Disposition"] = "attachment; filename=laststandcloud.tar.gz"
        response["X-Sendfile"] = "laststandcloud.tar.gz"
        return response

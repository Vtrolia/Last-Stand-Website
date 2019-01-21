from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import authenticate

import helpers as h


# Create your views here.
def index(request):
    pass


@csrf_exempt
@require_http_methods(["POST"])
def set_info(request, id):
    user, password = request.META["QUERY_STRING"].split("&")
    user = user.split("=")[1]
    password = h.sha256_hash(password.split("=")[1])

    if authenticate(request, username=user, password=password):
        return HttpResponse(content="Fuck you")

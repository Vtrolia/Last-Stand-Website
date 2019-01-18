from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return return_as_wanted(request, "home.html")


def rates(request):
    return return_as_wanted(request, "rates.html")


def login(request):
    if "USER" in request.session.keys():
        return redirect("/")
    else:
        return render(request, "login.html")


# not a view, this function is a helper so that the user can constantly be assured that they are still logged in
def return_as_wanted(request, template, message=None):
    if "USER" in request.session.keys():
        if "first_name" in request.session["USER"].keys():
            try:
                if len(request.session["USER"]["first_name"]) > 14:
                    request.session["USER"]["first_name"] = request.session["USER"]["first_name"][:11] + "..."
            except:
                pass
            return render(template, context={"name": "Welcome Back, " + str(request.session["USER"]["first_name"]) + "!",
                                             "message": message})

        greeting = ""
        if len(request.session["USER"]["username"]) > 14:
            greeting = request.session["USER"]["username"][:11] + "..."
        else:
            greeting = request.session["USER"]["username"]
        return render(request, template, context={"name": "Welcome Back, " + str(greeting) + "!", "message": message})

    return render(request, template)
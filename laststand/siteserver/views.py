from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "home.html")


def rates(request):
    return render(request, "rates.html")
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "index.html")


def ocsp(request):
    return render(request, "ocsp.html")


def statuses(request):
    return render(request, "account.html")
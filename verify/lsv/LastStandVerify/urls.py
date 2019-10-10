from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ocsp", views.ocsp, name="OCSP"),
    path("account", views.statuses, name="cert_statuses")
]

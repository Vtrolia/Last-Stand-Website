from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ocsp", views.ocsp, name="OCSP"),
    path("account", views.statuses, name="cert_statuses"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("submit_login", views.submit_login, name="submit_login")
]

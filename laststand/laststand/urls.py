"""laststand URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from siteserver import views as sv

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", sv.index, name="index"),
    path("rates", sv.rates, name="rates"),
    path("login", sv.login_page, name="login_page"),
    path("signup", sv.register_page, name="register_page"),
    path("submit-login", sv.submit_login, name="submit_login"),
    path("submit-register", sv.submit_register, name="submit_register"),
    path("more-info", sv.more_info, name="more_info"),
    path("add-name", sv.add_name, name="add_name"),
    path("logout", sv.logout_user, name="logout_user")
]

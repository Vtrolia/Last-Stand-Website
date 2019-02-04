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
from django.urls import path, include
from siteserver import views as sv

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", sv.index, name="index"),
    path("rates", sv.rates, name="rates"),
    path("login", sv.login_page, name="login_page"),
    path("download", sv.downloads, name="first_download_page"),
    path("signup", sv.register_page, name="register_page"),
    path("publish", sv.publish_page, name="publish_page"),
    path("issues", sv.issue_page, name="issue_page"),
    path("license", sv.license_page, name="license_page"),
    path("password-reset-page", sv.password_page, name="password_page"),
    path("account-settings", sv.account_page, name="account_page"),
    path("submit-login", sv.submit_login, name="submit_login"),
    path("submit-register", sv.submit_register, name="submit_register"),
    path("submit-article", sv.submit_article, name="submit_article"),
    path("submit-issue", sv.submit_issue, name="submit_issue"),
    path("submit-download", sv.submit_download, name="submit_download"),
    path("more-info", sv.more_info, name="more_info"),
    path("add-name", sv.add_name, name="add_name"),
    path("logout", sv.logout_user, name="logout_user"),
    path("relog", sv.relog_page, name="relog"),
    path("stories", sv.story, name="our_story"),
    path("get-articles", sv.load_articles, name="load_articles"),
    path("cloud-options-page", sv.load_cloud_options, name="load_cloud_options"),
    path("base-options-page", sv.load_base_options, name="load_base_options"),
    path("change-plan-page", sv.load_change_plan, name="load_plan_page"),
    path("api/", include("api.urls"))

]

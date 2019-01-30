from django.urls import path
from . import views

urlpatterns = [
    path("update-server/<name>", views.set_info, name="update_server"),
    path("forward-to-server/<name>", views.get_address, name="forward_to_server"),
    path("get-certificate/<name>", views.get_ssl_cert, name="get_ssl_cert"),
    path("renew-certificate/<name>", views.renew_cert, name="renew_cert"),
    path("submit-cloud/", views.submit_cloud, name="submit_cloud")
]
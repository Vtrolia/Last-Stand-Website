from django.urls import path
from . import views

urlpatterns = [
    path("update-server/<name>", views.set_info, name="update_server"),
    path("forward-to-server/<name>", views.get_address, name="forward_to_server"),
    path("is-valid/<name>", views.is_cert_valid, name="is_valid"),
    path("get-certificate/<name>", views.get_ssl_cert, name="get_ssl_cert"),
    path("get-user-cloud-info", views.get_user_info, name="user_cloud_info"),
    path("renew-certificate/<name>", views.renew_cert, name="renew_cert"),
    path("submit-cloud", views.submit_cloud, name="submit_cloud"),
    path("verify", views.verify, name="verify")
]
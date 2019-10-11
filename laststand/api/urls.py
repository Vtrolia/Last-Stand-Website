from django.urls import path
from . import views

urlpatterns = [
    path("update-server/<name>", views.set_info, name="update_server"),
    path("forward-to-server/<name>", views.get_address, name="forward_to_server"),
    path("get-user-clouds", views.get_user_clouds, name="get_user_clouds"),
    path("get-user-cloud-info", views.get_user_info, name="user_cloud_info"),
    path("verify", views.verify, name="verify"),
    path("delete-cloud", views.delete_cloud, name="delete_cloud"),
    path("download-client", views.download_client, name="download_client"),
    path("submit-cloud", views.submit_cloud, name="submit_cloud"),
    path("verify/login", views.lsverify_login, name="lsverify_login")
]

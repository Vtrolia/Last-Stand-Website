from django.urls import path
from . import views

urlpatterns = [
    path("update-server/<id>", views.set_info, name="update_server")
]
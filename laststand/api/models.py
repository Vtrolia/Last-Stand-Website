from django.contrib.auth.models import User
from django.db import models

# Create your models here:


# data needed to be stored in order to allow clouds to be remote accessed and secure
class Cloud(models.Model):
    id = models.TextField(primary_key=True, unique=True)
    port = models.IntegerField(default=8675)
    ip_address = models.CharField(max_length=30)
    remote_address = models.CharField(max_length=30)
    name = models.CharField(max_length=40, default=id)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    status = models.IntegerField(choices=((0, "Basic"), (1, "Family"), (2, "Business")), default=0)
    users = models.ManyToManyField(User, related_name="users_allowed")
    cert_renew = models.DateField(null=True)
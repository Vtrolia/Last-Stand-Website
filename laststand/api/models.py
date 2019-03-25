from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# keep track of important data of the generated SSL certificates W/OpenSSL, so that Last Stand's website can act like
# a CA for clouds
class SSL(models.Model):
    cacert = models.TextField(null=False, unique=True)
    created_by = models.ForeignKey(User, related_name="creator_user", on_delete=models.DO_NOTHING)
    date_created = models.DateField(null=False)
    date_expires = models.DateField(null=False)
    owned_by = models.ForeignKey(User, related_name="owner_user", null=True, on_delete=models.CASCADE)
    privkey = models.TextField(null=False, unique=True)


# data needed to be stored in order to allow clouds to be remote accessed and secure
class Cloud(models.Model):
    id = models.TextField(primary_key=True, unique=True)
    ip_address = models.CharField(max_length=30)
    name = models.CharField(max_length=40, default=id)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    ssl_cert = models.ForeignKey(SSL, on_delete=models.DO_NOTHING)
    status = models.IntegerField(choices=((0, "Basic"), (1, "Family"), (2, "Business")), default=0)
    users = models.ManyToManyField(User, related_name="users_allowed")
    
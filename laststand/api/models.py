from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# keep track of important data of the generated SSL certificates W/OpenSSL, so that Last Stand's website can act like
# a CA for clouds
class SSL(models.Model):
    privkey = models.TextField(null=False, unique=True)
    cacert = models.TextField(null=False, unique=True)
    date_created = models.DateField(null=False)
    date_expires = models.DateField(null=False)
    created_by = models.ForeignKey(User, related_name="creator_user", on_delete=models.DO_NOTHING)
    owned_by = models.ForeignKey(User, related_name="owner_user", null=True, on_delete=models.CASCADE)


# data needed to be stored in order to allow clouds to be remote accessed and secure
class Cloud(models.Model):
    id = models.TextField(primary_key=True, unique=True)
    name = models.CharField(max_length=40, default=id)
    given_name = models.TextField(default=name)
    ip_address = models.CharField(max_length=30)
    ssl_cert = models.ForeignKey(SSL, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="users_allowed")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    status = models.IntegerField(choices=((0, "Basic"), (1, "Family"), (2, "Business")), default=0)
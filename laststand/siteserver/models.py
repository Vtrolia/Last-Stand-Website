from django.db import models


# articles on the home page
class Articles(models.Model):
    date = models.CharField(max_length=40)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image_src = models.CharField(max_length=50)
    image_title = models.CharField(max_length=200)
    text = models.TextField()


# regular users who will just use their own clouds
class BaseUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    date_joined = models.DateField()
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=60)
    username = models.TextField()
    password = models.TextField()
    email = models.EmailField()


# optimizes searching for a publisher by only querying for the logged in user in this database instead of querying
# the entire BaseUsers database for whether or not they are allowed to publish
class PublisherUsers(models.Model):
    user_id = models.ForeignKey(BaseUser, on_delete=models.CASCADE)


# data needed to be stored in order to allow clouds to be remote accessed and secure
class Cloud(models.Model):
    id = models.TextField(primary_key=True, unique=True)
    ip_address = models.CharField(max_length=20)
    ssl_cert = models.TextField()
    users = models.ManyToManyField(BaseUser, related_name="users_allowed")
    owner = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="owner")




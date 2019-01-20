from django.db import models
from django.contrib.auth.models import User


# articles on the home page
class Articles(models.Model):
    date = models.CharField(max_length=40)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image_src = models.CharField(max_length=50)
    image_title = models.CharField(max_length=200)
    text = models.TextField()
    confirmed = models.BooleanField(default=False)

    def asJSON(self):
        return {
            "date": self.date,
            "author": self.author,
            "title": self.title,
            "image_src": self.image_src,
            "image_title": self.image_title,
            "content": self.text
        }


# optimizes searching for a publisher by only querying for the logged in user in this database instead of querying
# the entire BaseUsers database for whether or not they are allowed to publish
class PublisherUsers(models.Model):
    base_user = models.IntegerField()


# data needed to be stored in order to allow clouds to be remote accessed and secure
class Cloud(models.Model):
    id = models.TextField(primary_key=True, unique=True)
    ip_address = models.CharField(max_length=20)
    ssl_cert = models.TextField()
    users = models.ManyToManyField(User, related_name="users_allowed")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")




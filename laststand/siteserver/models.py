from django.db import models
from django.contrib.auth.models import User


# articles on the home page
class Articles(models.Model):
    author = models.CharField(max_length=100)
    confirmed = models.BooleanField(default=False)
    date = models.CharField(max_length=40)
    image_src = models.CharField(max_length=50, null=True, blank=True)
    image_title = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField()
    title = models.CharField(max_length=100)
    
    # send articles to the front end as JSON objects
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
    base_user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="id")







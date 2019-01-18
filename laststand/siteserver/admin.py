from django.contrib import admin
from siteserver import models

# Register your models here.
admin.site.register(models.Articles)
admin.site.register(models.BaseUser)
admin.site.register(models.Cloud)
admin.site.register(models.PublisherUsers)
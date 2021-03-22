from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Channel(models.Model):
    title = models.CharField(null=False, blank=False,
                             max_length=50, default="title here")
    location = models.IntegerField(default=95818) # TODO: change this
    # to better location system
    members = models.ManyToManyField(User)

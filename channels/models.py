from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Channel(models.Model):
    title = models.TextField(
        null=False,
        blank=False,
        max_length=50,
        default="title here",
        unique=True,
    )
    # location = models.IntegerField(default=95818) # TODO: change this
    location = models.TextField(
        null=False,
        blank=False,
        max_length=50000,
        default="no channel location inserted from html"
    )
    # to better location system
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.title

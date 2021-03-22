from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    creater = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(null=False, blank=False,
                             max_length=50, default="title here")
    message = models.CharField(null=False, blank=False,
                             max_length=50, default="message here")
    created_at = models.DateTimeField(
        auto_now=True
    )

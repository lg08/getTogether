from django.db import models

from django.contrib.auth.models import User
from channels.models import Channel

# Create your models here.


class Post(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        default="title here"
    )
    message = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        default="message here"
    )
    created_at = models.DateTimeField(
        auto_now=True
    )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
    )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_comments',
        blank=True,
        null=True
    )
    comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='comment_comments',
        blank=True,
        null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )
    message = models.TextField(
        max_length=200
    )
    created_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "{} commented '{}'".format(self.user, self.message)

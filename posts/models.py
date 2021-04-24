from django.db import models

from django.contrib.auth.models import User
from channels.models import Channel

# Create your models here.



class Post(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.TextField(
        null=False,
        blank=False,
        max_length=50,
        default="title here"
    )
    message = models.TextField(
        null=False,
        blank=False,
        max_length=1000,
        default="message here"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
    )
    num_of_upvotes = models.IntegerField(default=0)
    num_of_downvotes = models.IntegerField(default=0)
    num_of_comments = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    location = models.TextField(null=False, blank=False,
                                max_length=50000, default="put JSON" + \
                                "object here")

    def __str__(self):
        return self.title


class Event(models.Model):
    # creator = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE
    # )
    title = models.TextField(
        null=False,
        blank=False,
        max_length=50,
        default="title here"
    )
    message = models.TextField(
        null=False,
        blank=False,
        max_length=1000,
        default="message here"
    )
    # created_at = models.DateTimeField(
    #     auto_now_add=True
    # )
    num_of_upvotes = models.IntegerField(default=0)
    num_of_downvotes = models.IntegerField(default=0)
    num_of_comments = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    # start_time = models.DateTimeField()
    # end_time = models.DateTimeField()


    start_time = models.TextField(max_length=500)
    end_time = models.TextField(max_length=500)

    exact_location = models.TextField(null=False, blank=False,
                                      max_length=50000, default='{"latitude":40.344149988101236,"longitude":-74.65598258598506}')

    def __str__(self):
        return self.post.title

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
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "{} commented '{}'".format(self.user, self.message)


class Upvote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return "{} upvoted {}".format(self.user, self.post)


class Downvote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return "{} downvoted {}".format(self.user, self.post)

# def delete_all():
#     events = Event.objects.all()
#     for event in events:
#         event.delete()

# delete_all()

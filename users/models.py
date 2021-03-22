from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(null=False, blank=False,
                                 max_length=50, default="full name here")
    location = models.IntegerField(default=95818) # TODO: change this
    # to better location system

    def __str__(self):
        return "{}'s profile".format(self.user)

    # got this stuff from here: https://simpleisbetterthancomplex.com/tutorial/
    # 2016/07/22/how-to-extend-django-user-model.html
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()



class Event(models.Model):
    title = models.CharField(null=False, blank=False,
                             max_length=50, default="title here")
    description = models.CharField(
        null=False, blank=False,
        max_length=50,
        default="description here"
    )
    location = models.IntegerField(default=95818) # TODO: change this
    # to better location system
    start_time = models.DateTimeField(
        auto_now=True
    )
    end_time = models.DateTimeField(
        auto_now=False
    )

from django.contrib.auth.models import User
from posts.models import Post, Event
import json

def check_database():
    for user in User.objects.all():
        print(user.profile.location)
        try:
            json.loads(user.profile.location)
            if user.profile.location == "" or user.profile.location == "95818":
                user.profile.location = '{"latitude":40.3505454,"longitude":-74.652204}'
                user.profile.save()
        except:
            print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            print(user)
            user.profile.location = '{"latitude":40.3505454,"longitude":-74.652204}'
            user.profile.save()

    for post in Post.objects.all():
        print(post.location)
        try:
            json.loads(post.location)
        except:
            print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            print(post)
            post.location = '{"latitude":40.3505454,"longitude":-74.652204}'
            post.save()

    for event in Event.objects.all():
        print(event.exact_location)
        try:
            json.loads(event.exact_location)
        except:
            print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            print(event)

check_database()

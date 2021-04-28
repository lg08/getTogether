from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from . import forms
from django.contrib.auth.models import User
from posts.models import Post, Upvote, Downvote
from channels.models import Channel
from channels.views import haversine

import json

# Create your views here.

# posts = Post.objects.all()
# for post in posts:
#     if post.location == "put JSONobject here":
#         post.location = '{"latitude":40.3447222,"longitude":-74.7163889}'
#         post.save()


def profile_page(request, user_pk, columns=1, no_location=0):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=user_pk)
        channel_subscriptions = user.channel_set.all()
        posts = Post.objects.filter(creator__pk=user.pk)

        post_distance_list = []
        user_location = json.loads(request.user.profile.location)
        for post in posts:
            post_location = json.loads(post.location)
            distance = haversine(user_location['longitude'],
                                 user_location['latitude'],
                                 post_location['longitude'],
                                 post_location['latitude'])
            post_distance_list.append((post, int(distance)))
        upvotes = []
        downvotes = []
        if (request.user.is_authenticated):

            for i, post in enumerate(posts):
                upvotes.append(str(Upvote.objects.filter(user=request.user, post=posts[i])))
                downvotes.append(str(Downvote.objects.filter(user=request.user, post=posts[i])))

        context = {
            "this_user": user,
            "channel_subscriptions": channel_subscriptions,
            "posts": post_distance_list,
            "columns": columns,
            'upvotes': upvotes,
            'downvotes': downvotes,
            'no_location': no_location,
        }
        return render(request, "users/profile_page.html", context)
    else:
        return HttpResponseRedirect(
            reverse("users:login")
        )

def change_location(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            location = request.POST.get("user_location")
            request.user.profile.location = location
            request.user.profile.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            pass
    else:
        return HttpResponseRedirect(
            reverse("users:login")
        )



def signup(request):
    if request.method == 'POST':
        form = forms.UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.full_name = form.cleaned_data.get('full_name')
            user.profile.location = request.POST.get("userlocation")
            user.save()
            user.profile.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            # return redirect('users:profile_page', pk=request.user.pk)
            try:
                json.loads(user.profile.location)
                return HttpResponseRedirect(
                    reverse("home")
                )
            except:
                # default user location
                user.profile.location = '{"latitude":40.3447222,"longitude":-74.7163889}'
                user.profile.save()
                user.save()
                return HttpResponseRedirect(
                    reverse(
                        "users:profile_page",
                        kwargs={
                            'user_pk':user.pk,
                            'no_location': 1,
                        }
                    )
                )

    else:
        form = forms.UserCreateForm()
    return render(request, 'users/signup.html', {'form': form})

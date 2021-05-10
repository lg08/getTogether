from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from posts.models import Post, Upvote, Downvote
from .models import Channel
from django.views.generic.edit import CreateView

import json

from .forms import Channel_Create_Form

from math import radians, cos, sin, asin, sqrt

from GetTogether.views import check_login

# Create your views here.

def set_post_defaults():
    all_posts = Post.objects.all()
    for post in all_posts:
        post.location = '{"latitude":40.3505454,"longitude":-74.652204}'
        post.save()


def list_channels(request):
    authed = check_login(request)
    if authed != None:
        return authed
    all_channels = Channel.objects.all()
    nearby_channels = []
    user_location = json.loads(request.user.profile.location)
    for channel in all_channels:
        if channel.title != "Main" and channel.title != "Events":
            channel_location = json.loads(channel.location)
            distance = haversine(user_location['longitude'],
                                user_location['latitude'],
                                channel_location['longitude'],
                                channel_location['latitude'])
            if distance < 150:
                nearby_channels.append((channel, int(distance)))
    nearby_channels = sorted(nearby_channels, key = lambda x: x[1])
    context = {
        "channels": nearby_channels,
    }
    return render(request, "channels/list_channels.html", context)

def join_channel(request, channel_pk, join_or_remove):
    authed = check_login(request)
    if authed != None:
        return authed
    channel = get_object_or_404(Channel, pk=channel_pk)
    if join_or_remove == 1:
        channel.members.add(request.user)
    else:
        channel.members.remove(request.user)
    channel.save()
    return redirect(request.META['HTTP_REFERER'])


def create_channel(request):
    authed = check_login(request)
    if authed != None:
        return authed
    if request.method == 'POST':
        form = Channel_Create_Form(request.POST)
        if form.is_valid():
            try:
                json.loads(request.POST.get("channellocation"))
            except:
                context = {
                    "form": form,
                    "no_location": True,
                }
                return render (request, "channels/channel_form.html", context)
            new_channel = Channel()
            new_channel.title = form.cleaned_data['title']
            try:
                new_channel.save()  # have to keep this here to add the member
                new_channel.members.add(request.user)
                new_channel.location = request.POST.get("channellocation")
                new_channel.save()
                return HttpResponseRedirect(
                    reverse("channels:posts", kwargs={
                        "channel_pk": new_channel.pk,
                    })
                )
            except:
                context = {
                    "form": form,
                    "same_name": True,
                    }
                return render (request, "channels/channel_form.html", context)
        else:
            context = {
                "form": form,
            }
        return render (request, "channels/channel_form.html", context)
    # it's a "GET"
    else:
        form = Channel_Create_Form()
        context = {
            "form": form,
        }
        return render (request, "channels/channel_form.html", context)


def channel_posts(request, channel_pk=1, columns=0):
    this_channel = get_object_or_404(Channel, pk=channel_pk)
    all_channel_posts = Post.objects.filter(
        channel=this_channel
    ).order_by('-score')
    upvotes = []
    downvotes = []
    post_distance_list = []
    if request.user.is_authenticated:
        user_location = json.loads(request.user.profile.location)
    for i, post in enumerate(all_channel_posts):
        if request.user.is_authenticated:
            upvotes.append(str(Upvote.objects.filter(user=request.user, post=all_channel_posts[i])))
            downvotes.append(str(Downvote.objects.filter(user=request.user, post=all_channel_posts[i])))
            post_location = json.loads(post.location)
            distance = int(haversine(user_location['longitude'],
                                user_location['latitude'],
                                post_location['longitude'],
                                post_location['latitude']))
            if this_channel.title == "Main":
                if distance < 100:
                    post_distance_list.append((post, distance))
        else:
            distance = "Unknown"
            post_distance_list.append((post, distance))
    all_channel_users = this_channel.members.all()
    if request.user in this_channel.members.all():
        isin_channel = True
    else:
        isin_channel = False
    context = {
        'posts': post_distance_list,
        'channel_name': this_channel.title,
        'channel_members': all_channel_users,
        'channel': this_channel,
        'isin_channel': isin_channel,
        'columns': columns,
        'upvotes': upvotes,
        'downvotes': downvotes,
    }
    return render(request, "channels/channel.html", context)


def main_feed(request):
    # grabs the main channel
    main_channel = get_object_or_404(Channel, title='Main')
    # grabs all the posts associated with the main channel
    all_main_feed_posts = Post.objects.filter(
        channel=main_channel
    )
    upvotes = []
    downvotes = []
    if (request.user.is_authenticated):
        for i, post in enumerate(all_main_feed_posts):
            upvotes.append(str(Upvote.objects.filter(user=request.user, post=all_main_feed_posts[i])))
            downvotes.append(str(Downvote.objects.filter(user=request.user, post=all_main_feed_posts[i])))
    context = {
        'posts': all_main_feed_posts,
        'upvotes': upvotes,
        'downvotes': downvotes,
    }
    return render(request,  "index.html", context)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

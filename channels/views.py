from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from posts.models import Post
from .models import Channel
from django.views.generic.edit import CreateView

from .forms import Channel_Create_Form

from math import radians, cos, sin, asin, sqrt

# Create your views here.

def list_channels(request):
    all_channels = Channel.objects.all()
    context = {
        "channels": all_channels,
    }
    return render(request, "channels/list_channels.html", context)

def create_channel(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Channel_Create_Form(request.POST)
            if form.is_valid():
                new_channel = Channel()
                new_channel.title = form.cleaned_data['title']
                # new_channel.location = form.cleaned_data['location']
                new_channel.save()  # have to keep this here to add the member
                new_channel.members.add(request.user)
                new_channel.location = request.POST.get("channellocation")
                new_channel.save()

                # return HttpResponseRedirect(
                #     reverse("bets:detail", kwargs={"pk": new_bet.pk})
                # )
                return HttpResponseRedirect(
                    reverse("home")
                )
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
    else:
        return HttpResponseRedirect(
            reverse("users:login")
        )


def channel_posts(request, channel_pk):
    this_channel = get_object_or_404(Channel, pk=channel_pk)
    all_channel_posts = Post.objects.filter(
        channel=this_channel
    )
    all_channel_users = this_channel.members.all()
    context = {
        'posts': all_channel_posts,
        'channel_name': this_channel.title,
        'channel_members': all_channel_users,
        'channel': this_channel,
    }
    return render(request,  "channels/channel.html", context)


def main_feed(request):
    # if request.user.is_authenticated:
    # grabs the main channel
    main_channel = get_object_or_404(Channel, title='main')
    # grabs all the bets associated with the main channel
    all_main_feed_posts = Post.objects.filter(
        channel=main_channel
    )

    context = {
        'posts': all_main_feed_posts,
    }

    return render(request,  "index.html", context)
    # else:
        # if the user isn't loggin in, take them to the login page
        # return HttpResponseRedirect(reverse('users:login'))
        # pass



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

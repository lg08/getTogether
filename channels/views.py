from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from posts.models import Post
from .models import Channel
from django.views.generic.edit import CreateView

from .forms import Channel_Create_Form


# Create your views here.

# class-based view for creating a channel
# class ChannelCreate(CreateView):
#     model = Channel
#     fields = ['title', 'location']
#     # renders "channel_form.html"

def create_channel(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Channel_Create_Form(request.POST)
            if form.is_valid():
                new_channel = Channel()
                new_channel.title = form.cleaned_data['title']
                new_channel.location = form.cleaned_data['location']
                new_channel.members.add(request.user)
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
            reverse("home")
        )




def main_feed(request):
    # if request.user.is_authenticated:
    # grabs the main channel
    main_channel = get_object_or_404(Channel, title='main')
    # grabs all the bets associated with the main channel
    all_main_feed_posts = Post.objects.filter(
        channel=main_channel
    )

    context = {
        'main_feed_posts': all_main_feed_posts,
    }

    return render(request,  "index.html", context)
    # else:
        # if the user isn't loggin in, take them to the login page
        # return HttpResponseRedirect(reverse('users:login'))
        # pass

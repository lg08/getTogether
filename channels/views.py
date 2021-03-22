from django.shortcuts import render

from posts.models import Post
from .models import Channel
from django.views.generic.edit import CreateView


# Create your views here.

# class-based view for creating a channel
class ChannelCreate(CreateView):
    model = Channel
    fields = ['title', 'location']
    # renders "channel_form.html"



def main_feed(request):
    if request.user.is_authenticated:
        # grabs the main channel
        main_channel = Channel.objects.filter(
            title='main'
        )
        # grabs all the bets associated with the main channel
        all_main_feed_posts = Post.objects.filter(
            channel=main_channel
        )

        context = {
            'main_feed_posts': all_main_feed_posts,
        }

        return render(request,  "index.html", context)
    else:
        # if the user isn't loggin in, take them to the login page
        # return HttpResponseRedirect(reverse('users:login'))
        pass

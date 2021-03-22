from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import PostForm
from .models import Post
from channels.models import Channel

# Create your views here.

def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                new_post = Post()
                new_post.title = form.cleaned_data['title']
                new_post.message = form.cleaned_data['message']
                associated_channel = get_object_or_404(Channel, title=form.cleaned_data['channel'])
                new_post.channel = associated_channel
                new_post.creator = request.user
                new_post.save()
                return HttpResponseRedirect(
                    reverse("home")
                )
            # form not valid
            else:
                context = {
                    "form": form,
                }
                return render (request, "posts/post_create_form.html", context)
        # it's a get request
        else:
            form = PostForm()
            context = {
                "form": form,
            }
            return render (request, "posts/post_create_form.html", context)
    # user not logged in
    else:
        return HttpResponseRedirect(reverse('users:login'))

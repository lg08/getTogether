from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from . import forms
from django.contrib.auth.models import User
from posts.models import Post
from channels.models import Channel

# Create your views here.


def profile_page(request, user_pk, columns=1):
    user = get_object_or_404(User, pk=user_pk)
    channel_subscriptions = user.channel_set.all()
    posts = Post.objects.filter(creator__pk=user.pk)
    context = {
        "this_user": user,
        "channel_subscriptions": channel_subscriptions,
        "posts": posts,
        "columns": columns,
    }
    return render(request, "users/profile_page.html", context)


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
            return HttpResponseRedirect(
                reverse("home")
            )
    else:
        form = forms.UserCreateForm()
    return render(request, 'users/signup.html', {'form': form})

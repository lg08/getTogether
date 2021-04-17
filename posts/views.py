from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .forms import PostForm
from .models import Post, Upvote, Downvote
from channels.models import Channel

from .redditUpDownAlg import hot

# Create your views here.

def create_post(request, channel):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                new_post = Post()
                new_post.title = form.cleaned_data['title']
                new_post.message = form.cleaned_data['message']
                associated_channel = get_object_or_404(Channel, pk=channel)
                new_post.channel = associated_channel
                new_post.creator = request.user
                new_post.save()
                new_post.score = hot(0, 0, new_post.created_at)
                new_post.save()
                return HttpResponseRedirect(reverse('channels:posts', kwargs={'channel_pk': channel}))
            # form not valid
            else:
                context = {
                    "form": form,
                    "channel": get_object_or_404(Channel, pk=channel),
                }
                return render (request, "posts/post_create_form.html", context)
        # it's a get request
        else:
            form = PostForm()
            context = {
                "form": form,
                "channel": get_object_or_404(Channel, pk=channel),
            }
            return render (request, "posts/post_create_form.html", context)
    # user not logged in
    else:
        return HttpResponseRedirect(reverse('users:login'))


def upvote_downvote_post(request, postid, up_or_downvote):
    if request.user.is_authenticated:
        this_post = get_object_or_404(Post, pk=postid)
        if up_or_downvote == "upvote":
            new_vote, created = Upvote.objects.get_or_create(
                user=request.user,
                post=this_post
            )
            if created:
                this_post.num_of_upvotes += 1
                new_vote.user = request.user
                new_vote.post = this_post
                new_vote.save()
                # delete the downvote if there is one
                try:
                    downvote = Downvote.objects.get(post=this_post, user=request.user)
                    downvote.delete()
                    this_post.num_of_downvotes -= 1
                except:
                    pass
            else:
                this_post.num_of_upvotes -= 1
                new_vote.delete()
        elif up_or_downvote == 'downvote':
            new_vote, created = Downvote.objects.get_or_create(
                user=request.user,
                post=this_post
            )
            if created:
                this_post.num_of_downvotes += 1
                new_vote.user = request.user
                new_vote.post = this_post
                new_vote.save()
                # delete the upvote if there is one
                try:
                    upvote = Upvote.objects.get(post=this_post, user=request.user)
                    upvote.delete()
                    this_post.num_of_upvotes -= 1
                except:
                    pass
            else:
                this_post.num_of_downvotes -= 1
                new_vote.delete()
        this_post.save()
        this_post.score = hot(this_post.num_of_upvotes,
                              this_post.num_of_downvotes,
                              this_post.created_at)
        this_post.save()
        this_post.refresh_from_db()
        data = {
            "postid": this_post.id,
            "upvotes": this_post.num_of_upvotes,
            "downvotes": this_post.num_of_downvotes,
            "created": created,
        }
        return JsonResponse(data, safe=False)
        # return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('users:login'))

from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from channels.views import haversine

from .forms import PostForm, CommentForm, EventForm
from .models import Post, Upvote, Downvote, Comment, Event
from channels.models import Channel

from .redditUpDownAlg import hot

import json

# Create your views here.


def create_comment(request, postpk, commentpk, subcomment):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=postpk)
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                if subcomment == 1:  # it's a subcomment
                    new_comment.comment = get_object_or_404(Comment, pk=commentpk)
                    new_comment.post = post
                    new_comment.user = request.user
                    new_comment.save()
                    post.num_of_comments += 1
                    post.save()
                else:
                    new_comment.post = post
                    new_comment.user = request.user
                    new_comment.save()
                    post.num_of_comments += 1
                    post.save()
                return HttpResponseRedirect(reverse('posts:detail',
                                                    kwargs={"postpk": post.pk}
                                                    ))
    else:
        return HttpResponseRedirect(reverse('users:login'))

def post_detail(request, postpk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=postpk)
        context = {
            "post": post,
            "comment_form": CommentForm,
        }
        return render(request, "posts/post_detail.html", context)
    else:
        return HttpResponseRedirect(reverse('users:login'))

def view_events(request):
    if request.user.is_authenticated:
        all_events = Event.objects.all()
        # for event in all_events:
        #     event.delete()
        user_location = json.loads(request.user.profile.location)
        nearby_posts = []
        for event in all_events:
            event_location = json.loads(event.exact_location)
            distance = haversine(user_location['longitude'],
                                user_location['latitude'],
                                event_location['longitude'],
                                event_location['latitude'])
            nearby_posts.append((event, int(distance)))

        context = {
            "posts": nearby_posts,
        }
        return render (request, "posts/all_events.html", context)
    else:
        return HttpResponseRedirect(reverse('users:login'))


def create_event(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print("is inside post")
            form = EventForm(request.POST)
            if form.is_valid():
                print("form is valid")
                new_event = Event()
                new_event.title = form.cleaned_data['title']
                new_event.message = form.cleaned_data['message']
                new_event.creator = request.user
                new_event.save()
                new_event.score = hot(0, 0, new_event.created_at)
                new_event.save()
                new_event.start_time = json.dumps(request.POST.get("start_time"))
                new_event.end_time = json.dumps(request.POST.get("end_time"))
                new_event.exact_location = request.POST.get("channellocation")
                new_event.save()
                return HttpResponseRedirect(reverse('posts:detail', kwargs={'postpk': new_post.pk}))
            # form not valid
            else:
                print("form not valid")
                print(form.errors)
                context = {
                    "form": form,
                    # "channel": get_object_or_404(Channel, pk=channel),
                }
                return render (request, "posts/event_form.html", context)
        # it's a get request
        else:
            form = EventForm()
            context = {
                "form": form,
                # "channel": get_object_or_404(Channel, pk=channel),
            }
            return render (request, "posts/event_form.html", context)

    else:
        return HttpResponseRedirect(reverse('users:login'))


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
                new_post.location = request.user.profile.location
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

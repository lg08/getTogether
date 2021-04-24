from django.urls import path

from . import views

app_name = 'posts'


urlpatterns = [
    path(
        'create_post/<int:channel>/',
        views.create_post,
        name='create'
    ),
    path(
        '<slug:up_or_downvote>/<int:postid>/',
        views.upvote_downvote_post,
        name='up_or_downvote'
    ),
    path(
        "<int:postpk>/detail/",
        views.post_detail,
        name='detail'
    ),
    path(
        'create/comment/<int:subcomment>/on/<int:postpk>/<int:commentpk>/',
        views.create_comment,
        name='create_comment'
    ),
    path(
        'create_event/',
        views.create_event,
        name='create_event'
    ),
    path(
        'view_events/',
        views.view_events,
        name='events'
    ),
]

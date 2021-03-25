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
]

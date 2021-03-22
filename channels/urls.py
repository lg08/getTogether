from django.urls import path
from . import views


app_name = 'channels'


urlpatterns = [
    path(
        'create/',
        views.create_channel,
        name='create',
    ),
    path(
        'all/',
        views.list_channels,
        name='list'
    ),
    path(
        '<int:channel_pk>/',
        views.channel_posts,
        name='posts'
    ),
]

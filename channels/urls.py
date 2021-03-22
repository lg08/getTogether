from django.urls import path
from . import views


app_name = 'channels'


urlpatterns = [
    path(
        'create/',
        views.ChannelCreate.as_view(),
        name='create_channel',
    )
]

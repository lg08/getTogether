from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'users'

urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('signup/',
         views.signup,
         name='signup'),
    path('logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),
    path(
        'profile_page/<int:user_pk>/',
        views.profile_page,
        name='profile_page'
    ),
    path(
        'profile_page/<int:user_pk>/<int:columns>/',
        views.profile_page,
        name='profile_page'
    ),

]

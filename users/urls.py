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
    path(
        "change_location/",
        views.change_location,
        name='change_location'
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name='users/passwordReset.html'), 
        name='password_reset',
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name='users/passwordResetDone.html'), 
        name='password_reset_done',
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name='users/reset.html'), 
        name='password_reset_confirm'
    ),
    path(
        "reset/done/", 
        auth_views.PasswordResetCompleteView.as_view(template_name='users/resetDone.html'), 
        name='password_reset_complete'
    )

]

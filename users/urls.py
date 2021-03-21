from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'users'

urlpatterns = [
    # path('login/',
    #      auth_views.LoginView.as_view(template_name='users/login.html'),
    #      name='login'),
    # path('signup/',
    #      views.signup,
    #      name='signup'),
    # path('logout/',
    #      auth_views.LogoutView.as_view(),
    #      name='logout'),
    # path('profile/of/<int:pk>/',
    #      views.user_profile_page,
    #      name='profile_page'),
    # path(
    #     'add_friend/<int:friendpk>',
    #     views.add_friend,
    #     name='add_friend'
    # ),
    # path(
    #     'remove_friend/<int:friendpk>',
    #     views.remove_friend,
    #     name='remove_friend'
    # ),
    # path(
    #     'search/',
    #     views.search_results,
    #     name='search'
    # ),
    # path(
    #     'change-password/',
    #     auth_views.PasswordChangeView.as_view(template_name='users/change_password.html'),
    #     name='change_password'
    # ),

    # path('authorize/', StripeAuthorizeView.as_view(), name='authorize'),

    # path('oauth/callback/', StripeAuthorizeCallbackView.as_view(), name='authorize_callback'),
]

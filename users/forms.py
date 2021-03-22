from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserCreateForm(UserCreationForm):
    # birthdate = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    full_name = forms.CharField(max_length=50)
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Public Username"
        self.fields['email'].label = "Email Address"

# for email confirmation
# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

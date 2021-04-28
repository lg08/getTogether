from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Channel_Create_Form(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={"rows":1, "style":"width:100%;"}))
    # location = forms.IntegerField()

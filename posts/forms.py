from django import forms

class PostForm(forms.Form):
    title = forms.CharField()
    message = forms.CharField()
    channel = forms.CharField()

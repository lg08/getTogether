from django import forms

class PostForm(forms.Form):
    title = forms.CharField()
    message = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'post_message_form'}
        )
    )
    channel = forms.CharField()

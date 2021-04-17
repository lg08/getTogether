from django import forms
from channels.models import Channel
from posts.models import Comment

CHOICES = []
for channel in Channel.objects.all():
    CHOICES.append((channel, channel))


class PostForm(forms.Form):
    title = forms.CharField()
    message = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'post_message_form'}
        )
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message', )

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


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class TimeInput(forms.TimeInput):
    input_type = "time"


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class EventForm(forms.Form):
    title = forms.CharField()
    message = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'post_message_form'}
        )
    )

    start_time = forms.CharField(
        # input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    end_time = forms.CharField(
        # input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        })
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message', )

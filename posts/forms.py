from django import forms
from channels.models import Channel
from posts.models import Comment

CHOICES = []
for channel in Channel.objects.all():
    CHOICES.append((channel, channel))


class PostForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={"rows":1, "style":"width:100%;"}))
    # message = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'post_message_form',
    #             # 'size': '20',
    #             'style': 'width: 100%;',
    #             'rows': 5,
    #             'cols': 15,
    #         }
    #     )
    # )
    # message.widget.attrs.update(size='60')
    message= forms.CharField(widget=forms.Textarea(attrs={"rows":5, "style":"width:100%;"}))



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
    title = forms.CharField(widget=forms.Textarea(attrs={"rows":1, "style":"width:100%;"}))
    message= forms.CharField(widget=forms.Textarea(attrs={"rows":5, "style":"width:100%;"}))

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

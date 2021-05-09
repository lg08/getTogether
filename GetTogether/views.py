from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'index.html'


def check_login(request):
    if request.user.is_authenticated:
        pass
    else:
        return HttpResponseRedirect(reverse('users:login'))

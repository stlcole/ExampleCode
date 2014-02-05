from django.contrib.auth import logout
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.shortcuts import render

from .forms import ParticipantCreationForm, ParticipantLoginForm


def logout_view(request):
    logout(request)
    return HttpResponse('Logged out')


class ParticipantLoginFormView(FormView):
    # template_name = 'login.html'
    form_class = ParticipantLoginForm
    initial = {}
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, self.get_context_data(form=form))


class ParticipantCreationFormView(FormView):
    # template_name = 'setup.html'
    form_class = ParticipantCreationForm
    initial = {}
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return HttpResponse('Is Valid')

    def get(self, request, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, self.get_context_data(form=form))
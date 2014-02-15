from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from braces.views import LoginRequiredMixin
from class_based_auth_views.views import LoginView

from .forms import ParticipantCreationForm, ParticipantLoginForm, ProfileChangeForm
from .models import Profile


class ParticipantLoginFormView(LoginView):
    template_name = 'participant/login.html'
    form_class = ParticipantLoginForm
    initial = {}

    def get_success_url(self):
        return '/participant/{}'.format(self.request.user.profile.slug)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        self.set_test_cookie()
        return render(request, self.template_name, self.get_context_data(form=form))


class ParticipantCreationFormView(FormView):
    template_name = 'participant/setup.html'
    form_class = ParticipantCreationForm
    initial = {}
    success_url = '/participant/profile/change/'

    def form_valid(self, form):
        user = form.save()
        return super(ParticipantCreationFormView, self).form_valid(form)

    def get(self, request, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, self.get_context_data(form=form))


class ProfileChangeView(LoginRequiredMixin, FormView):
    template_name = 'participant/change_profile.html'
    form_class = ProfileChangeForm
    initial = {}

    def get_success_url(self):
        return '/participant/{}'.format(self.request.user.profile.slug)

    def form_valid(self, form):
        form.participant_id = self.request.user.id
        form.save()
        return super(ProfileChangeView, self).form_valid(form)

    def get(self, request, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, self.get_context_data(form=form))


class ProfileView(LoginRequiredMixin, TemplateView):
    model = Profile
    queryset = Profile.objects.all()
    context_object_name = "participant"
    template_name = 'participant/profile.html'

    def get(self, request, **kwargs):
        context = self.get_context_data()

        try:
            slug = context['view'].kwargs['slug']
            if Profile.objects.get(slug=slug).id != self.request.user.profile.id:
                return HttpResponse("Here be dragon: you aren't authorized to see the requested Profile")

            return render(request, self.template_name, context)

        except Profile.DoesNotExist:
            return HttpResponseRedirect('/participant/profile/change/')
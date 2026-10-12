from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from problems.models import ProblemStatus
from accounts.views import aggregate_problems

class LandingPage(TemplateView):
    template_name = 'core/landing_page.html'


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['calendar'] = False
        context['title'] = 'Home'
        context |= aggregate_problems(self.request.user)

        unlocked_topics = self.request.user.unlocked_topics.filter(usertopic__status='UNLOCKED')
        context['unlocked_topics'] = unlocked_topics

        context['problems_in_progress'] = ProblemStatus.objects.filter(user=self.request.user, status='IN_PROGRESS')
        context['starred_problems'] = ProblemStatus.objects.filter(user=self.request.user, starred=True)

        return context


class Resources(TemplateView):
    template_name = 'core/resources.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['calendar'] = False
        context['title'] = 'Resources'

        if self.request.user.is_authenticated:
            context['base_template'] = 'accounts/base.html'

        else:
            context['base_template'] = 'accounts/base2.html'

        return context
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class HomePageView(LoginRequiredMixin, TemplateView):
    """
    Home page view
    """
    login_url = reverse_lazy('login')
    template_name = "home.html"
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

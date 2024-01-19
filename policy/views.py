from django.shortcuts import render
from django.views.generic import TemplateView


class PolicyTemplateView(TemplateView):
    template_name = 'policy/policy.html'

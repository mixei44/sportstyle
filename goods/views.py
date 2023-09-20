from django.shortcuts import render
from django.views.generic import TemplateView

class CatalogTemplateView(TemplateView):
    template_name = 'goods/catalog.html'
    
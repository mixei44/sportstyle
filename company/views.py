from django.shortcuts import render
from django.views.generic import TemplateView


class AboutTemplateView(TemplateView):
    template_name = 'company/about.html'

class ShopTemplateView(TemplateView):
    template_name = 'company/shop.html'

class PartnerTemplateView(TemplateView):
    template_name = 'company/partner.html'

class ObuvTemplateView(TemplateView):
    template_name = 'company/obuv.html'

class JacketTemplateView(TemplateView):
    template_name = 'company/jacket.html'

class TrouserTemplateView(TemplateView):
    template_name = 'company/trouser.html'

class TermobeleTemplateView(TemplateView):
    template_name = 'company/termobele.html'

class DzhemperTemplateView(TemplateView):
    template_name = 'company/dzhemper.html'




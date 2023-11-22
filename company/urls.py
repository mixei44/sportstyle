from django.urls import path
from .views import AboutTemplateView, ShopTemplateView, PartnerTemplateView, ObuvTemplateView, JacketTemplateView, TrouserTemplateView, TermobeleTemplateView, DzhemperTemplateView

urlpatterns = [
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('shops/', ShopTemplateView.as_view(), name='shop'),
    path('partners/', PartnerTemplateView.as_view(), name='partner'),
    path('obuv/', ObuvTemplateView.as_view(), name='obuv'),
    path('jacket/', JacketTemplateView.as_view(), name='jacket'),
    path('trouser/', TrouserTemplateView.as_view(), name='trouser'),
    path('termobele/', TermobeleTemplateView.as_view(), name='termobele'),
    path('dzhemper/', DzhemperTemplateView.as_view(), name='dzhemper'),

]

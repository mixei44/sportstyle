from django.urls import path
from .views import CatalogTemplateView


urlpatterns = [
    path('', CatalogTemplateView.as_view()),
]
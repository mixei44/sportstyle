from django.urls import path

from .views import PolicyTemplateView

urlpatterns = [
    path('', PolicyTemplateView.as_view(), name='policy')
]
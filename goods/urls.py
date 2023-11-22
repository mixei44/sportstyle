from django.urls import path
from .views import CatalogTemplateView, ProductListView


urlpatterns = [
    path('<str:category>/', ProductListView.as_view(), name='product'),
    path('', CatalogTemplateView.as_view(), name='catalog'),
]

from django.urls import path
from .views import CatalogView, ProductListView, ProductDetailView


urlpatterns = [
    path('<str:category>/', ProductListView.as_view(), name='products'),
    path('<str:category>/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('', CatalogView.as_view(), name='catalog'),
]

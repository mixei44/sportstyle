from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import CATEGORY
from .service import FILTERS


class CatalogTemplateView(TemplateView):
    template_name = 'goods/catalog.html'


class ProductListView(ListView):
    def get(self, request: HttpRequest, category) -> HttpResponse:
        if category not in [key for key in CATEGORY.keys()]:
            raise Http404('Указана неизвестная категория товара')
        goods = CATEGORY[category].objects.all()
        ProductFilter = FILTERS.get(category)
        f = ProductFilter(request.GET, queryset=goods)
        return render(request, 'goods/product.html', {'filter': f})

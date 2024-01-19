from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import ListView
from django.views import View

from .models import CATEGORY, CATEGORY_TRANSLATE
from .service import FILTERS


class ProductListView(ListView):
    def get(self, request: HttpRequest, category) -> HttpResponse:
        if category not in [key for key in CATEGORY.keys()]:
            raise Http404('Указана неизвестная категория товара')
        goods = CATEGORY[category].objects.all()
        ProductFilter = FILTERS.get(category)
        f = ProductFilter(request.GET, queryset=goods)
        return render(request, 'goods/products.html', {'filter': f, 'category': category})


class ProductDetailView(View):
    def get(self, request: HttpRequest, category, pk):
        if category not in [key for key in CATEGORY.keys()]:
            raise Http404('Указана неизвестная категория товара')
        product = CATEGORY[category].objects.filter(pk=pk)
        if not product.exists():
            raise Http404('Указан неизвестный идентификатор товара')
        return render(request, 'goods/{0}.html'.format(category), {'product': product[0], 'category': CATEGORY_TRANSLATE.get(category, '')})


class CatalogView(View):
    def get(self, request: HttpRequest):
        products = {
            'shoes': CATEGORY['shoes'].objects.all()[:2],
            'jacket': CATEGORY['jacket'].objects.all()[:2],
            'trousers': CATEGORY['trousers'].objects.all()[:2],
            'thermal': CATEGORY['thermal'].objects.all()[:2],
            'jumper': CATEGORY['jumper'].objects.all()[:2],
        }
        return render(request, 'goods/catalog.html', {'products': products})

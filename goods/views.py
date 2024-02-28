from django.http import HttpRequest, HttpResponse, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import ListView
from django.views import View

from .models import CATEGORY, CATEGORY_TRANSLATE
from .service import FILTERS


class ProductListView(ListView):
    def get(self, request: HttpRequest, category) -> HttpResponse:
        if category not in [key for key in CATEGORY.keys()]:
            raise Http404('Указана неизвестная категория товара')
        goods = CATEGORY[category].objects.all().prefetch_related('photos')
        ProductFilter = FILTERS.get(category)
        products_qs = ProductFilter(request.GET, queryset=goods)
        products_qs_form = products_qs.form
        products_qs = products_qs.qs
        
        paginator = Paginator(products_qs, 15)
        page, num_pages = request.GET.get('page'), paginator.num_pages
        try:
            response = paginator.page(page)
            page = int(page)
        except PageNotAnInteger:
            response = paginator.page(1)
            page = 1
        except EmptyPage:
            response = paginator.page(num_pages)
        if num_pages <= 11 or page <= 6:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page - 5, page + 6)]
        return render(request, 'goods/products.html', {
            'filter': response,  'filter_form': products_qs_form, 'category': category, 'pages': pages
        })


class ProductDetailView(View):
    def get(self, request: HttpRequest, category, pk):
        if category not in [key for key in CATEGORY.keys()]:
            raise Http404('Указана неизвестная категория товара')
        product = CATEGORY[category].objects.filter(pk=pk).prefetch_related('photos')
        if not product.exists():
            raise Http404('Указан неизвестный идентификатор товара')
        return render(request, 'goods/{0}.html'.format(category), {'product': product[0], 'category': CATEGORY_TRANSLATE.get(category, '')})


class CatalogView(View):
    def get(self, request: HttpRequest):
        products = {
            'shoes': CATEGORY['shoes'].objects.all()[:2].prefetch_related('photos'),
            'jacket': CATEGORY['jacket'].objects.all()[:2].prefetch_related('photos'),
            'trousers': CATEGORY['trousers'].objects.all()[:2].prefetch_related('photos'),
            'thermal': CATEGORY['thermal'].objects.all()[:2].prefetch_related('photos'),
            'jumper': CATEGORY['jumper'].objects.all()[:2].prefetch_related('photos'),
        }
        return render(request, 'goods/catalog.html', {'products': products})

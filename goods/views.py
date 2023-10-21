from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import ShoesModel, JacketModel
from .service import ShoesFilter, JacketFilter


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CatalogTemplateView(TemplateView):
    template_name = 'goods/catalog.html'


class ShoesFilteredListView(FilteredListView):
    model = ShoesModel
    paginate_by = 20
    filterset_class = ShoesFilter
    context_object_name = 'shoes'
    template_name = 'goods/shoes.html'


class JacketFilteredListView(FilteredListView):
    model = JacketModel
    paginate_by = 20
    filterset_class = JacketFilter
    context_object_name = 'jackets'
    template_name = 'goods/jacket.html'

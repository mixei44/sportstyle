import django_filters

from .models import ShoesModel, JacketModel


class FilterMixin(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        fields = ('gender', 'age_type', 'title')


class ShoesFilter(FilterMixin, django_filters.FilterSet):
    # title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta(FilterMixin.Meta):
        model = ShoesModel
        # fields = ('gender', 'age_type')


class JacketFilter(FilterMixin, django_filters.FilterSet):
    class Meta(FilterMixin.Meta):
        model = JacketModel
        # fields = ('', )
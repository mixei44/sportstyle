import django_filters
from django import forms

from .models import BrandModel, ShoesModel, JacketModel, TrouserModel, ThermalUnderwearModel, JumperModel


class FilterMixin(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    price = django_filters.RangeFilter(field_name='price')
    brand = django_filters.ModelMultipleChoiceFilter(field_name='brand', queryset=BrandModel.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        fields = ( 'title', 'gender', 'age_type', 'sport_type', 'season', 'price', 'brand')


class ShoesFilter(FilterMixin, django_filters.FilterSet):
    class Meta(FilterMixin.Meta):
        model = ShoesModel


class JacketFilter(FilterMixin, django_filters.FilterSet):
    class Meta(FilterMixin.Meta):
        model = JacketModel


class TrouserModel(FilterMixin, django_filters.FilterSet):
    class Meta(FilterMixin.Meta):
        model = TrouserModel


class ThermalUnderwearModel(FilterMixin, django_filters.FilterSet):
    class Meta(FilterMixin.Meta):
        model = ThermalUnderwearModel
        fields = ( 'title', 'gender', 'age_type', 'price', 'brand')


class JumperModel(FilterMixin, django_filters.FilterSet):
    class Meta(FilterMixin.Meta):
        model = JumperModel
        fields = ( 'title', 'gender', 'age_type', 'season', 'price', 'brand')


FILTERS = {
    'shoes': ShoesFilter,
    'jacket': JacketFilter,
    'trousers': TrouserModel,
    'thermal': ThermalUnderwearModel,
    'jumper': JumperModel,
}

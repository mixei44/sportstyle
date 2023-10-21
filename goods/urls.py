from django.urls import path
from .views import CatalogTemplateView, ShoesFilteredListView, JacketFilteredListView


urlpatterns = [
    path('shoes/', ShoesFilteredListView.as_view(), name='shoes'),
    path('', JacketFilteredListView.as_view(), name='catalog'),
]












# import django_filters

# class PostFilter(django_filters.FilterSet):
#     class Meta:
#         model = Post
#         fields = ['author']
# the view:

# from django_filters.views import FilterView
# from somwhere.in.your.project.filtersets import PostFilter

# class PostList(FilterView):
#     model = Post
#     context_object_name = 'posts'
#     filter_class = PostFilter
# in template:

# {% extends "base.html" %}

# {% block content %}
#     <form action="" method="get">
#         {{ filter.form.as_p }}
#         <input type="submit" />
#     </form>
#     {% for obj in filter.qs %}
#         {{ obj.name }} - ${{ obj.price }}<br />
#     {% endfor %}
# {% endblock %}
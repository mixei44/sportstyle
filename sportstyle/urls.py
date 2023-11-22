from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('company/', include('company.urls')),
    path('', include('goods.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'SportStyle'
admin.site.index_title = 'Администрирование SportStyle'

# handler404 = 'sportstyle.views.custom_404'
# handler500 = 'sportstyle.views.custom_500'

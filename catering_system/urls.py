from django.contrib import admin
from django.urls import path, include
from users.views import landing_redirect
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='urls')),
    path('orders/', include('orders.urls')),
    path('menu/', include('menu.urls', namespace='menu')),
    path('bulk_orders/', include('bulk_orders.urls')),
    # path('delivery/', include('delivery.urls')),
    # path('reports/', include('reports.urls')),
    path('', landing_redirect),
    path('payments/', include(('payments.urls', 'payments'), namespace='payments')),
    
    path('preparation/', include('preparation.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
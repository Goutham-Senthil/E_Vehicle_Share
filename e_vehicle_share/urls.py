from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing_start.urls')),
    path('customers/', include('customers.urls')),
    path('operators/', include('operators.urls')),
    path('managers/', include('managers.urls')),
]

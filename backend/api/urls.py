from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('healthcheck.urls')),
    path('api/account', include('account.urls')),
]

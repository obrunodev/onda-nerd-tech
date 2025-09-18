from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('accounts/', include('apps.accounts.urls')),
    path('admin/', admin.site.urls),
    path('finance/', include('apps.finance.urls')),
]

from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from mailing.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Главная страница
    path('mailing/', include('mailing.urls', namespace='mailing')),
]

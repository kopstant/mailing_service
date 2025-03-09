from django.urls import path

from .apps import MailingConfig
from .views import RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView, RecipientDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('recipient/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/new/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/<int:pk>/edit/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),
]

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from mailing.forms import RecipientForm
from mailing.models import Recipient, Mailing, Message


# CRUD для модели Получатель рассылки
class RecipientListView(ListView):  # Список объектов.
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'


class RecipientDetailView(DetailView):  # Детали конкретного объекта
    model = Recipient
    template_name = 'mailing/recipient_detail.html'
    context_object_name = 'recipient'


class RecipientCreateView(CreateView):  # Создание
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')


class RecipientUpdateView(UpdateView):  # Изменение
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')


class RecipientDeleteView(DeleteView):  # Удаление
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')


# CRUD для модели Управления сообщениями
class MessageListView(ListView):  # Список объектов.
    model = Message


class MessageDetailView(DetailView):  # Детали конкретного объекта
    model = Message


class MessageCreateView(CreateView):  # Создание
    model = Message


class MessageUpdateView(UpdateView):  # Изменение
    model = Message


class MessageDeleteView(DeleteView):  # Удаление
    model = Message


# CRUD для модели Рассылка
class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing


class MailingDeleteView(DeleteView):
    model = Mailing

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.models import Recipient, Mailing, Message


# CRUD для модели Получатель рассылки
class RecipientListView(ListView):  # Список объектов.
    model = Recipient


class RecipientDetailView(DetailView):  # Детали конкретного объекта
    model = Recipient


class RecipientCreateView(CreateView):  # Создание
    model = Recipient


class RecipientUpdateView(UpdateView):  # Изменение
    model = Recipient


class RecipientDeleteView(DeleteView):  # Удаление
    model = Recipient


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

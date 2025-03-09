from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from mailing.forms import RecipientForm, MessageForm, MailingForm
from mailing.models import Recipient, Mailing, Message, TryMailing


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
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'


class MessageDetailView(DetailView):  # Детали конкретного объекта
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(CreateView):  # Создание
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView):  # Изменение
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView):  # Удаление
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')


# CRUD для модели Рассылка
class MailingListView(ListView):  # Список объектов.
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'


class MailingDetailView(DetailView):  # Детали конкретного объекта
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(CreateView):  # Создание
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(UpdateView):  # Изменение
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(DeleteView):  # Удаление
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.send_mails():
        messages.success(request, "Рассылка успешно отправлена!")
    else:
        messages.error(request, "Ошибка отправки рассылки.")

    return redirect('mailing_list')


def mailing_report(request):
    attempts = TryMailing.objects.all().order_by('-attempt_time')
    return render(request, 'mailing/mailing_report.html', {'attempts': attempts})


def home_view(request):
    """Главная страница со статистикой"""
    total_mailings = Mailing.objects.count()  # Всего рассылок
    active_mailings = Mailing.objects.filter(status='started').count()  # Кол-во активных рассылок
    unique_recipients = Recipient.objects.distinct().count()  # Уникальные получатели

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_recipients': unique_recipients,
    }
    return render(request, 'mailing/home.html', context)

import datetime

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Recipient(models.Model):
    email = models.CharField(unique=True, max_length=100, verbose_name='email')
    full_name = models.CharField(max_length=100, verbose_name="full Name", **NULLABLE)
    comments = models.TextField(verbose_name="comments", **NULLABLE)

    def __str__(self):
        return self.email


class Message(models.Model):
    subject_of_the_letter = models.CharField(max_length=100, verbose_name="subject of the letter", **NULLABLE)
    letter_body = models.TextField(verbose_name="letter body", **NULLABLE)

    def __str__(self):
        return self.subject_of_the_letter


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]
    # Дата и время первой отправки
    first_sent_at = models.DateTimeField(auto_now_add=True, verbose_name="date created")
    # Дата и время окончания отправки
    end_sent_at = models.DateTimeField(verbose_name="date and time ending")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Создана', verbose_name="status")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="message")
    recipients = models.ManyToManyField(Recipient, verbose_name="recipients")

    def __str__(self):
        return f'Рассылка {self.status} - {", ".join([recipient.email for recipient in self.recipients.all()])}'

from django.db import models
from users.models import CustomUser

NULLABLE = {'blank': True, 'null': True}


# Модель получателя рассылки
class Recipient(models.Model):
    email = models.EmailField(unique=True, max_length=100, verbose_name='email')
    full_name = models.CharField(max_length=100, verbose_name="full Name", **NULLABLE)
    comments = models.TextField(verbose_name="comments", **NULLABLE)
    owner = models.ForeignKey(CustomUser, verbose_name="Owner", on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'Recipient'
        verbose_name_plural = 'Recipients'
        permissions = []

    def __str__(self):
        return self.email


# Модель сообщения
class Message(models.Model):
    subject_of_the_letter = models.CharField(max_length=100, verbose_name="subject of the letter", **NULLABLE)
    letter_body = models.TextField(verbose_name="letter body", **NULLABLE)
    owner = models.ForeignKey(CustomUser, verbose_name="Owner", on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        permissions = []

    def __str__(self):
        return self.subject_of_the_letter


# Модель рассылки
class Mailing(models.Model):
    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'

    STATUS_CHOICES = (
        (COMPLETED, 'Завершена'),
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
    )
    # Дата и время первой отправки
    first_sent_at = models.DateTimeField(verbose_name="date created", **NULLABLE)
    # Дата и время окончания отправки
    end_sent_at = models.DateTimeField(verbose_name="date and time ending", **NULLABLE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="status")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="message")
    recipients = models.ManyToManyField(Recipient, verbose_name="recipients")
    owner = models.ForeignKey(CustomUser, verbose_name="Owner", on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'
        ordering = ['message', 'owner']
        permissions = []

    def __str__(self):
        return f'Рассылка {self.status} - {", ".join([recipient.email for recipient in self.recipients.all()])}'


# Модель попытки рассылки
class TryMailing(models.Model):
    SUCCESS = 'success'
    FAILURE = 'failure'

    STATUS_CHOICES = (
        (SUCCESS, 'Успешно'),
        (FAILURE, 'Не успешно'),
    )

    created_at = models.DateTimeField(verbose_name="date created")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="status")
    response = models.TextField(verbose_name="response")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="message", related_name="attempts")

    class Meta:
        verbose_name = 'Attempt Mailing'
        verbose_name_plural = 'Attempts Mailings'

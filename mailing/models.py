from django.db import models
from django.utils.timezone import now

from users.models import CustomUser
from django.core.mail import send_mail
from django.db import models


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
    last_sent = models.DateTimeField(null=True, blank=True, verbose_name="Дата последней отправки")

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'
        ordering = ['message', 'owner']
        permissions = []

    def __str__(self):
        return f'Рассылка {self.status} - {self.first_sent_at} - {self.end_sent_at}'

    def send_mails(self):
        """Отправляет письма и фиксирует попытки рассылки"""
        if self.status == self.COMPLETED:
            return False  # Нельзя отправлять завершенные рассылки

        recipient_list = self.recipients.all()
        if not recipient_list:
            return False  # Нет получателей

        success_count = 0

        for recipient in recipient_list:
            try:
                send_mail(
                    subject=self.message.subject_of_the_letter,
                    message=self.message.letter_body,
                    from_email='kopstant@icloud.com',  # Заменить на свой email
                    recipient_list=[recipient.email],
                    fail_silently=False
                )
                TryMailing.objects.create(
                    mailing=self,
                    status='Успешно',
                    server_response="Письмо успешно отправлено",
                )
                success_count += 1

            except Exception as e:
                TryMailing.objects.create(
                    mailing=self,
                    status='Не успешно',
                    server_response=str(e),
                )

        self.last_sent = now()
        if success_count > 0:
            self.status = self.STARTED  # Если были успешные отправки, статус "Запущена"
        self.save()
        return True


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
    response = models.TextField(verbose_name="response", **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="mailing", related_name="attempts")

    class Meta:
        verbose_name = 'Attempt Mailing'
        verbose_name_plural = 'Attempts Mailings'

    def __str__(self):
        return f'{self.status} - {self.created_at} - {self.response}'

from django.contrib import admin
from .models import Recipient, Message, Mailing


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comments', 'owner')
    search_fields = ('email', 'full_name', 'owner')

    def get_owner(self, obj):
        return obj.owner if obj.owner else 'Нет владельца'
    get_owner.short_description = 'Owner'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject_of_the_letter', 'letter_body', 'owner')
    search_fields = ('subject_of_the_letter', 'owner')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('first_sent_at', 'end_sent_at', 'status', 'message', 'owner')
    search_fields = ('status', 'message__subject')
    list_filter = ('status', 'owner')

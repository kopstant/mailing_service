from django.contrib import admin
from .models import Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comments', 'owner')
    search_fields = ('email', 'full_name', 'owner')

    def get_owner(self, obj):
        return obj.owner if obj.owner else 'Нет владельца'
    get_owner.short_description = 'Owner'

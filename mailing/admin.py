from django.contrib import admin
from .models import Recipient, Message, Mailing, TryMailing
from django.utils.html import format_html


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

    def send_button(self, obj):
        if obj.status == 'CREATED':
            return format_html('<a class="button" href="/admin/mailing/mailing/{}/send/">Отправить</a>', obj.id)
        return "Уже отправлено"

    send_button.short_description = 'Отправка'
    send_button.allow_tags = True


@admin.register(TryMailing)
class TryMailingAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'status', 'response', 'mailing')
    list_filter = ('status', 'created_at')
    search_fields = ('mailing__status', 'response')

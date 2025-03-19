from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создает группу "Менеджеры" и назначает ей права доступа'

    def handle(self, *args, **kwargs):
        # Создаем группу
        group, created = Group.objects.get_or_create(name='Менеджеры')

        # Назначаем права
        mailing_permissions = Permission.objects.filter(codename__in=['can_view_all_mailings', 'can_disable_mailing'])
        recipient_permissions = Permission.objects.filter(codename='can_view_all_recipients')
        message_permissions = Permission.objects.filter(codename='can_view_all_messages')

        group.permissions.add(*mailing_permissions, *recipient_permissions, *message_permissions)
        self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана и права назначены.'))

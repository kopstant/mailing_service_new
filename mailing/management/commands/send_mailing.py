from django.core.management.base import BaseCommand
from mailing.models import Mailing


class Command(BaseCommand):
    help = 'Отправляет все ожидающие рассылки'

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status='CREATED')

        if not mailings.exists():
            self.stdout.write(self.style.WARNING("Нет рассылок для отправки."))
            return

        for mailing in mailings:
            if mailing.send_mails():
                self.stdout.write(self.style.SUCCESS(f"Рассылка {mailing.id} отправлена!"))
            else:
                self.stdout.write(self.style.ERROR(f"Ошибка отправки рассылки {mailing.id}."))

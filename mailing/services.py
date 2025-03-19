from django.core.cache import cache

from mailing.models import Recipient, Mailing, Message
from config.settings import CACHES_ENABLED


def get_recipient_from_cache():
    """Получает данные по  получателям рассылкам из кэша, если кэш пуст - получает данные из БД."""
    if not CACHES_ENABLED:
        return Recipient.objects.all()

    key = "recipies_list"
    recipies = cache.get(key)

    if recipies is None:
        # Получаем получателей из БД и сохраняем в кэш
        recipies = Recipient.objects.all()
        cache.set(key, recipies, timeout=1800)  # Cохраняем на 30 минут.
    return recipies


def get_messages_from_cache():
    """Получает данные по сообщениям из кэша, если кэш пуст - получает данные из БД."""
    if not CACHES_ENABLED:
        return Message.objects.all()

    key = "recipies_list"
    messages = cache.get(key)

    if messages is None:
        # Получаем сообщения из БД и сохраняем в кэш
        messages = Message.objects.all()
        cache.set(key, messages, timeout=1800)  # Cохраняем на 30 минут.
    return messages


def get_mailing_from_cache():
    """Получает данные по рассылкам из кэша, если кэш пуст - получает данные из БД."""
    if not CACHES_ENABLED:
        return Mailing.objects.all()

    key = "recipies_list"
    mailings = cache.get(key)

    if mailings is None:
        # Получаем рассылки из БД и сохраняем в кэш
        mailings = Mailing.objects.all()
        cache.set(key, mailings, timeout=1800)  # Cохраняем на 30 минут.
    return mailings

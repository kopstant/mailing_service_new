from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from mailing.forms import RecipientForm, MessageForm, MailingForm
from mailing.models import Recipient, Mailing, Message, TryMailing
from django.contrib.auth.mixins import LoginRequiredMixin

from mailing.services import get_recipient_from_cache, get_mailing_from_cache, get_messages_from_cache
from users.views import is_manager


# CRUD для модели Получатель рассылки
class RecipientListView(LoginRequiredMixin, ListView):  # Список объектов.
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджеры').exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, DetailView):  # Детали конкретного объекта
    model = Recipient
    template_name = 'mailing/recipient_detail.html'
    context_object_name = 'recipient'

    def get_queryset(self):
        return get_recipient_from_cache()


class RecipientCreateView(LoginRequiredMixin, CreateView):  # Создание
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_create.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):  # Изменение
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def get_form_class(self):
        user = self.request.user
        recipient = self.get_object()

        # Если пользователь - владелец, разрешаем полное редактирование
        if user == recipient.owner:
            return RecipientForm

        # Если пользователь - менеджер, разрешаем только просмотр
        if user.groups.filter(name='Менеджеры').exists():
            raise PermissionDenied("Менеджеры могут только просматривать получателей рассылки.")

        # Во всех остальных случаях запрещаем доступ
        raise PermissionDenied("У вас нет прав для редактирования.")


class RecipientDeleteView(LoginRequiredMixin, DeleteView):  # Удаление
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def get_object(self, queryset=None):
        # Получаем объект (рассылку)
        obj = super().get_object(queryset)
        user = self.request.user

        # Проверяем, может ли текущий пользователь удалить объект
        if user != obj.owner:
            # Если это не владелец, проверяем, состоит ли в группе менеджеров
            if user.groups.filter(name='Менеджеры').exists():
                raise PermissionDenied("Менеджеры не могут удалять рассылки.")
            else:
                raise PermissionDenied("У вас нет прав для удаления этой рассылки.")
        return obj


# CRUD для модели Управления сообщениями
class MessageListView(LoginRequiredMixin, ListView):  # Список объектов.
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджеры').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):  # Детали конкретного объекта
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        return get_messages_from_cache()


class MessageCreateView(LoginRequiredMixin, CreateView):  # Создание
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_create.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):  # Изменение
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def get_form_class(self):
        user = self.request.user
        message = self.get_object()

        # Если пользователь - владелец, разрешаем полное редактирование
        if user == message.owner:
            return MessageForm

        # Если пользователь - менеджер, разрешаем только просмотр
        if user.groups.filter(name='Менеджеры').exists():
            raise PermissionDenied("Менеджеры могут только просматривать получателей рассылки.")

        # Во всех остальных случаях запрещаем доступ
        raise PermissionDenied("У вас нет прав для редактирования.")


class MessageDeleteView(LoginRequiredMixin, DeleteView):  # Удаление
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        # Получаем объект (рассылку)
        obj = super().get_object(queryset)
        user = self.request.user

        # Проверяем, может ли текущий пользователь удалить объект
        if user != obj.owner:
            # Если это не владелец, проверяем, состоит ли в группе менеджеров
            if user.groups.filter(name='Менеджеры').exists():
                raise PermissionDenied("Менеджеры не могут удалять рассылки.")
            else:
                raise PermissionDenied("У вас нет прав для удаления этой рассылки.")
        return obj


# CRUD для модели Рассылка
class MailingListView(LoginRequiredMixin, ListView):  # Список объектов.
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):  # Детали конкретного объекта
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        return get_mailing_from_cache()


class MailingCreateView(LoginRequiredMixin, CreateView):  # Создание
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_create.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):  # Изменение
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_class(self):
        user = self.request.user
        mailings = self.get_object()

        # Если пользователь - владелец, разрешаем полное редактирование
        if user == mailings.owner:
            return MailingForm

        # Если пользователь - менеджер, разрешаем только просмотр
        if user.groups.filter(name='Менеджеры').exists():
            raise PermissionDenied("Менеджеры могут только просматривать получателей рассылки.")

        # Во всех остальных случаях запрещаем доступ
        raise PermissionDenied("У вас нет прав для редактирования.")


class MailingDeleteView(LoginRequiredMixin, DeleteView):  # Удаление
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        # Получаем объект (рассылку)
        obj = super().get_object(queryset)
        user = self.request.user

        # Проверяем, может ли текущий пользователь удалить объект
        if user != obj.owner:
            # Если это не владелец, проверяем, состоит ли в группе менеджеров
            if user.groups.filter(name='Менеджеры').exists():
                raise PermissionDenied("Менеджеры не могут удалять рассылки.")
            else:
                raise PermissionDenied("У вас нет прав для удаления этой рассылки.")
        return obj


def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.send_mails():
        messages.success(request, "Рассылка успешно отправлена!")
    else:
        messages.error(request, "Ошибка отправки рассылки.")

    return redirect('mailing:mailing_list')


def mailing_report(request):
    # Получаем все попытки текущего пользователя
    attempts = TryMailing.objects.filter(mailing__owner=request.user).order_by('-created_at')

    # Считаем успешные и неуспешные попытки
    success_count = TryMailing.objects.filter(mailing__owner=request.user, status=TryMailing.SUCCESS).count()
    failure_count = TryMailing.objects.filter(mailing__owner=request.user, status=TryMailing.FAILURE).count()

    # Общее количество отправленных сообщений
    total_messages = attempts.count()

    # Передаем данные в шаблон
    context = {
        'attempts': attempts,
        'success_count': success_count,
        'failure_count': failure_count,
        'total_messages': total_messages,
    }
    return render(request, 'mailing/mailing_report.html', context)


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


@user_passes_test(is_manager)
def cancel_mailing_view(request, pk):
    """Отменяет рассылку"""
    mailing = get_object_or_404(Mailing, pk=pk)

    # Отключаем рассылку
    mailing.status = 'disabled'  # Предположим, что у вас есть поле status
    mailing.save()

    messages.success(request, 'Рассылка отключена.')
    return redirect('mailing_list')  # Перенаправляем на список рассылок

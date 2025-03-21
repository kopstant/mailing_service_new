from django.contrib.auth import login
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import FormView, DetailView
from django.contrib import messages
from django.views.generic import ListView
from django.shortcuts import render

from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import redirect, get_object_or_404
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import CustomUser


class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'customusers'


# Профиль
class CustomUserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/customuser_profile.html'
    context_object_name = 'customuser_profile'

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = self.request.build_absolute_uri(f'verify/{uid}/{token}/')
        self.send_welcome_email(user.email, verification_link)
        return super().form_valid(form)

    def send_welcome_email(self, user_email, url):
        subject = 'Добро пожаловать в наш сервис!'
        message = f'Спасибо, что зарегистрировались в нашем сервисе! Подтвердите вашу почту по ссылке - {url}'
        from_email = 'testdmitrynadelyaev@yandex.ru'
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


def verify_email(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = CustomUser.objects.get(pk=uid)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(reverse('home'))
    return redirect(reverse('register'))  # Отдельная страничка с указанием


class CustomPasswordResetView(auth_views.PasswordResetView):  # Запрос на сброс пароля
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'  # В этом шаблоне письмо, которое придет на почту.
    success_url = reverse_lazy('users:password_reset_done')  # Должен уводить на страницу с подтверждением


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):  # Подтверждение сброса пароля
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')  # Должен уводить на страницу об успешном сбросе пароля


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    success_url = reverse_lazy('users:login')  # После успешного сброса пароля, переводит на страницу с логином.


def is_manager(user):
    return user.groups.filter(name='Менеджеры').exists()


@user_passes_test(is_manager)
def block_user(request, user_id):
    """
    Блокирует пользователя. Доступно только менеджерам.
    """
    user_to_block = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':

        # Переключаем статус блокировки
        user_to_block.is_blocked = not user_to_block.is_blocked
        user_to_block.is_active = not user_to_block.is_blocked  # Деактивируем пользователя, если он заблокирован
        user_to_block.save()

        if user_to_block.is_blocked:
            messages.success(request, f'Пользователь {user_to_block.email} заблокирован.')
        else:
            messages.success(request, f'Пользователь {user_to_block.email} разблокирован.')

    return redirect('home')


@login_required
def profile_edit(request):
    user = request.user  # Текущий пользователь

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            # Перенаправление на страницу профиля с user_id
            return redirect(reverse('users:user_profile', args=[user.id]))
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'users/profile_edit.html', {'form': form})

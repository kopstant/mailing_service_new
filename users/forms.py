from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=11, required=False)
    username = forms.CharField(max_length=50, required=True)
    avatar = forms.ImageField(required=False)
    usable_password = None

    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', 'phone_number', 'avatar', 'country', 'password1',
            'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите ваш e-mail'})
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите ваш логин'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите ваш номер телефона'})
        self.fields['avatar'].widget.attrs.update(
            {'class': 'avatar', 'placeholder': 'Выберите изображение для вашего профиля'})
        self.fields['country'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите вашу страну'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите пароль'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Подтвердите пароль'})

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Please enter a valid phone number. Only numbers are allowed.')
        return phone_number


class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        """Возвращает пользователя по email."""
        return CustomUser.objects.filter(email__iexact=email, is_active=True)


class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']

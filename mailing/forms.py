from django import forms
from mailing.models import Recipient, Message, Mailing


# Форма для получателя рассылки.
class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = [
            'email',
            'full_name',
            'comments',
            'owner'
        ]
        exclude = ['owner']


# Форма для работы с сообщением.
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'subject_of_the_letter',
            'letter_body',
            'owner',
        ]
        exclude = ['owner']


# Форма для рассылок
class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = [
            'first_sent_at',
            'end_sent_at',
            'status',
            'message',
            'recipients',
            'owner',
        ]
        exclude = ['owner']
        widgets = {
            'first_sent_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_sent_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

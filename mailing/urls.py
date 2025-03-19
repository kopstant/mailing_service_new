from django.urls import path

from .apps import MailingConfig
from .views import RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView, \
    RecipientDetailView, send_mailing_view, mailing_report, cancel_mailing_view
from .views import MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MessageDetailView
from .views import MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('recipient/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/new/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/<int:pk>/edit/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/new/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/new/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/send/', send_mailing_view, name='mailing_send'),
    path('mailings/report/', mailing_report, name='mailing_report'),
    path('mailings/<int:pk>/cancel/', cancel_mailing_view, name='cancel_mailing'),

]

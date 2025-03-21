from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
from users.views import RegisterView, verify_email, block_user, CustomPasswordResetCompleteView, CustomUserListView, \
    CustomUserProfileView, profile_edit

from .views import CustomPasswordResetView, CustomPasswordResetConfirmView, CustomPasswordResetDoneView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/verify/<uidb64>/<token>/', verify_email, name='verify_email'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('user/<int:user_id>/', CustomUserListView.as_view(), name='customuser_list'),
    path('user/<int:user_id>/block/', block_user, name='block_user'),
    path('profile/<int:user_id>/', CustomUserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
]

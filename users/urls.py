from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, CustomLogoutView, register

app_name = 'users'

urlpatterns = [
    # Autenticação
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),

    # Recuperação de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password.html',
        extra_context={'view_name': 'password_reset'}
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password.html',
        extra_context={'view_name': 'password_reset_done'}
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password.html',
        extra_context={'view_name': 'password_reset_confirm'}
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password.html',
        extra_context={'view_name': 'password_reset_complete'}
    ), name='password_reset_complete'),
]

from django.urls import path
from .views import (
    signup_view, signin_view, verify_email,
    admin_register_view, admin_login_view, verified_users_view,
    forgot_password_view, admin_verify_email
)

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
    path('admin-verify-email/<uuid:token>/', admin_verify_email, name='admin_verify_email'),
    path('admin/register/', admin_register_view, name='admin_register'),
    path('admin/login/', admin_login_view, name='admin_login'),
    path('admin/verified-users/', verified_users_view, name='verified_users'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
]

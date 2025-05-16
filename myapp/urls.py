from django.urls import path
from .views import signup_view, signin_view, verify_email

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
]

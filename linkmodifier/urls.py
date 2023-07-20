from django.urls import path
from .views import start_page, register, login

urlpatterns = [
    path('', start_page, name="start_page"),
    path('registration/', register, name="registration_page"),
    path('login/', login, name="login_page")
]
from django.urls import path
from .views import start_page, register, login_page, home_page, add_link, logout_view, add_qr
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', start_page, name="start_page"),
    path('registration/', register, name="registration_page"),
    path('login/', login_page, name="login_page"),
    path('homepage/', home_page, name="home_page"),
    path('addlink/', add_link, name="add_link"),
    path('logout/', logout_view, name="logout"),
    path('addQR/<int:pk>', add_qr, name="add_qr_page"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
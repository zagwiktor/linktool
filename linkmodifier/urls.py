from django.urls import path
from .views import start_page, register, login_page, home_page,\
    add_link, logout_view, add_qr, delete_link, edit_qr, delete_qr, add_shortened_link, shortened_link_redirect, delete_shortened_link

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
    path('deletelink/<int:pk>', delete_link, name="delete_link"),
    path('editQR/<int:pk>', edit_qr, name="edit_qr_page"),
    path('addShort/<int:pk>', add_shortened_link, name="add_shortened_link"),
    path('editQR/deleteQR/<int:pk>', delete_qr, name="delete_qr_page"),
    path('<str:slugs>/', shortened_link_redirect, name="short_redirect"),
    path('deleteShortLink/<int:pk>', delete_shortened_link, name="short_delete"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
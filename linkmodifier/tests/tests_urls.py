from django.test import SimpleTestCase
from django.urls import reverse, resolve
from linkmodifier.views import start_page, register, login_page, home_page, add_link, logout_view, add_qr, delete_link, edit_qr, delete_qr

class TestUrls(SimpleTestCase):
    def test_start_page_is_resolved(self):
        url = reverse('start_page')
        self.assertEqual(resolve(url).func, start_page)

    def test_registration_page_is_resolved(self):
        url = reverse('registration_page')
        self.assertEqual(resolve(url).func, register)

    def test_login_page_is_resolved(self):
        url = reverse('login_page')
        self.assertEqual(resolve(url).func, login_page)

    def test_logout_is_resolved(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout_view)

    def test_add_link_is_resolved(self):
        url = reverse('add_link')
        self.assertEqual(resolve(url).func, add_link)

    def test_home_page_is_resolved(self):
        url = reverse('home_page')
        self.assertEqual(resolve(url).func, home_page)

    def test_add_qr_page_is_resolved(self):
        url = reverse('add_qr_page', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, add_qr)

    def test_delete_link_is_resolved(self):
        url = reverse('delete_link', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, delete_link)

    def test_edit_qr_page_is_resolved(self):
        url = reverse('edit_qr_page', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, edit_qr)

    def test_delete_qr_page_is_resolved(self):
        url = reverse('delete_qr_page', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, delete_qr)

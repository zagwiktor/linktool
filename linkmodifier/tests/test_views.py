from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from linkmodifier.views import start_page, register, login_page
from django.http import HttpResponse
from django.contrib.auth.models import User
from linkmodifier.models import Link
from linkmodifier.forms import LinkForm
import base64
from PIL import Image
import io

class TestViews(TestCase):
    def test_start_page(self):
        request = RequestFactory().get(reverse('start_page'))
        response = start_page(request)
        try:
            template = get_template('linkmodifier/startpage.html')
        except TemplateDoesNotExist:
            template = None

        self.assertIsNotNone(template)
        self.assertEqual(response.status_code, 200)

    def test_register_get(self):
        request_get = RequestFactory().get(reverse('registration_page'))
        response_get = register(request_get)

        try:
            template = get_template('linkmodifier/registration.html')
        except TemplateDoesNotExist:
            template = None

        self.assertIsNotNone(template)
        self.assertEqual(response_get.status_code, 200)
        self.assertIsInstance(response_get, HttpResponse)

    def test_register_post_valid_form(self):
        data = {'username': 'testuser', 'password1': 'testpasword1', 'password2': 'testpasword1'}
        client = Client()
        response_post_valid = client.post(reverse('registration_page'), data)
        self.assertRedirects(response_post_valid, reverse('login_page'))

    def test_register_post_invalid_form(self):
        data_invalid_form = {}
        client = Client()
        response_post_invalid = client.post(reverse('registration_page'), data_invalid_form)
        self.assertIsInstance(response_post_invalid, HttpResponse)
        self.assertEqual(response_post_invalid.status_code, 200)

    def test_login_get(self):
        request = RequestFactory().get(reverse('login_page'))
        response_get = login_page(request)

        try:
            template = get_template('linkmodifier/login.html')
        except TemplateDoesNotExist:
            template = None

        self.assertIsNotNone(template)
        self.assertEqual(response_get.status_code, 200)
        self.assertIsInstance(response_get, HttpResponse)

    def test_login_post_valid_form(self):
        client = Client()
        user = User.objects.create_user(username='testuser', password='testpassword1')
        data = {'username': 'testuser', 'password': 'testpassword1'}
        response = client.post(reverse('login_page'), data)

        self.assertRedirects(response, reverse('home_page'))

    def test_login_post_invalid_form(self):
        client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword1')
        data = {'username': 'testuser', 'password': 'wrong_password'}
        response = client.post(reverse('login_page'), data)

        self.assertContains(response, "Username or password is incorrect")

    def test_home_page_authenticated_user(self):
        self.client = Client()
        url_link = reverse('home_page')
        self.user = User.objects.create_user(username='testuser', password='testpassword1')
        Link.objects.create(user=self.user, title='Test Link 1', url_link='http://example.com')
        Link.objects.create(user=self.user, title='Test Link 2', url_link='http://example.org')

        self.client.login(username='testuser', password='testpassword1')
        response = self.client.get(url_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Link 1')
        self.assertContains(response, 'Test Link 2')

    def test_home_page_unauthenticated_user(self):
        self.client = Client()
        self.home_url = reverse('home_page')

        response = self.client.get(self.home_url, follow=True)
        self.assertRedirects(response, '/login/?next=/homepage/')

    def test_add_link_get(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.add_link_url = reverse('add_link')
        response = self.client.get(self.add_link_url)


        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LinkForm)
        self.assertTemplateUsed(response, 'linkmodifier/addlink.html')

    def test_add_link_post(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.add_link_url = reverse('add_link')
        data = {
            'title': 'Test Link',
            'url_link': 'http://example.com',
        }
        response = self.client.post(self.add_link_url, data)
        self.assertRedirects(response, reverse('home_page'))
        self.assertEqual(Link.objects.count(), 1)
        new_link = Link.objects.first()
        self.assertEqual(new_link.title, 'Test Link')
        self.assertEqual(new_link.url_link, 'http://example.com')
        self.assertEqual(new_link.user, self.user)

    def test_add_qr_get(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.link = Link.objects.create(user=self.user, title='Test Link', url_link='http://example.com')
        self.add_qr_url = reverse('add_qr_page', args=[self.link.pk])

        response = self.client.get(self.add_qr_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'http://example.com')
        self.assertTemplateUsed(response, 'linkmodifier/add_qr.html')

    def test_add_qr_post(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.link = Link.objects.create(user=self.user, title='Test Link', url_link='http://example.com')
        self.add_qr_url = reverse('add_qr_page', args=[self.link.pk])

        response = self.client.post(self.add_qr_url)
        self.assertRedirects(response, reverse('home_page'))

    def test_delete_link_get(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.link = Link.objects.create(user=self.user, title='Test Link', url_link='http://example.com')
        self.delete_link_url = reverse('delete_link', args=[self.link.pk])

        response = self.client.get(self.delete_link_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'http://example.com')
        self.assertTemplateUsed(response, 'linkmodifier/delete.html')

    def test_delete_link_post(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.link = Link.objects.create(user=self.user, title='Test Link', url_link='http://example.com')
        self.delete_link_url = reverse('delete_link', args=[self.link.pk])

        response = self.client.post(self.delete_link_url)

        self.assertRedirects(response, reverse('home_page'))
        self.assertFalse(Link.objects.filter(pk=self.link.pk).exists())

    def test_edit_qr_get(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.link = Link.objects.create(user=self.user, title='Test Link', url_link='http://example.com')
        self.edit_qr_url = reverse('edit_qr_page', args=[self.link.pk])

        response = self.client.get(self.edit_qr_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'http://example.com')
        self.assertTemplateUsed(response, 'linkmodifier/edit_qr.html')

    def test_edit_qr_post(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.link = Link.objects.create(user=self.user, title='Test Link', url_link='http://example.com')
        self.edit_qr_url = reverse('edit_qr_page', args=[self.link.pk])

        response = self.client.post(self.edit_qr_url)

        self.assertRedirects(response, reverse('home_page'))


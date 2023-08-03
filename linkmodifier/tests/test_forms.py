from django.test import TestCase
from linkmodifier.forms import CreateNewUser, LinkForm

class FormTestCase(TestCase):
    def test_create_new_user_form(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = CreateNewUser(data=form_data)
        self.assertTrue(form.is_valid())

    def test_link_form(self):
        form_data = {
            'title': 'Test Link',
            'url_link': 'http://example.com',
        }
        form = LinkForm(data=form_data)
        self.assertTrue(form.is_valid())

from django.test import TestCase
from linkmodifier.models import Link
from django.contrib.auth.models import User

class LinkModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.link = Link.objects.create(
            title='Test Link',
            url_link='http://example.com',
            user=self.user,
            shortened_link='shortlink'
        )

    def test_model_str_method(self):
        self.assertEqual(str(self.link), 'http://example.com')

    def test_model_fields(self):
        self.assertEqual(self.link.title, 'Test Link')
        self.assertEqual(self.link.url_link, 'http://example.com')
        self.assertEqual(self.link.user, self.user)
        self.assertEqual(self.link.shortened_link, 'shortlink')



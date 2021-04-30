from importlib import import_module
from unittest import skip

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.store.models import Category, Product
from apps.store.views import all_products

User = get_user_model()


@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_exmaple(self):
        pass


class TestViewResponses(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django beginners',
                               created_by_id=1, slug='django-beginners',
                               price='20.00', image='django')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.client.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.client.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_category_list_url(self):
        """
        Test category response status
        """
        response = self.client.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test items response status
        """
        response = self.client.get(reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Example: code validation, search HTML for text
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Book Store</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        """
        Example: Using request factory
        """
        request = self.factory.get('/django-beginners')
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Book Store</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

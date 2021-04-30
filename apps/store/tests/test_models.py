from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.store.models import Category, Product
from core.utils import unique_slug_generator

User = get_user_model()


class TestCategoriesModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data1 = Category.objects.create(name='django', slug='django')
        cls.data2 = Category.objects.create(name='django')
        unique_slug_generator(cls.data2)

    def test_category_model_return(self):
        """
        Test Category model return name
        """
        data1 = self.data1
        data2 = self.data2
        self.assertIsInstance(data1, Category)
        self.assertIsInstance(data2, Category)
        self.assertEqual(str(data1), 'django')
        self.assertEqual(str(data2), 'django')

    def test_category_url(self):
        """
        Test category model slug and URL reverse
        """
        data = self.data1
        response = self.client.post(reverse('store:category_list', args=[data.slug]))
        self.assertEqual(response.status_code, 200)

    def test_category_unique_slug(self):
        data1 = self.data1
        data2 = self.data2
        self.assertNotEqual(data1.slug, data2.slug)


class TestProductsModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        cls.data1 = Product.objects.create(category_id=1,
                                           title='django beginners',
                                           created_by_id=1,
                                           slug='django-beginners',
                                           price='20.00',
                                           image='django')

        cls.data2 = Product.objects.create(category_id=1,
                                           title='django advanced',
                                           created_by_id=1,
                                           slug='django-advanced',
                                           price='10.00',
                                           image='django',
                                           is_active=False)

        cls.data3 = Product.objects.create(category_id=1,
                                           title='django beginners',
                                           created_by_id=1,
                                           price='40.00',
                                           image='django',
                                           is_active=False)
        unique_slug_generator(cls.data3)

    def test_products_model_return(self):
        """
        Test Category model return name
        """
        data = self.data1
        self.assertIsInstance(data, Product)
        self.assertEqual(str(data), 'django beginners')

    def test_products_url(self):
        """
        Test product model slug and URL reverse
        """
        data = self.data1
        response = self.client.post(reverse('store:product_detail', args=[data.slug]))
        self.assertEqual(response.status_code, 200)

    def test_product_unique_slug(self):
        data1 = self.data1
        data2 = self.data2
        data3 = self.data3
        self.assertNotEqual(data1.slug, data2.slug, data3.slug)

    def test_products_custom_manager_basic(self):
        """
        Test product model custom manager returns only active products
        """
        data = Product.objects.all()
        self.assertEqual(data.count(), 1)

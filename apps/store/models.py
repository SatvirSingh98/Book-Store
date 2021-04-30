from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

from core.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category_list', kwargs={'slug': self.slug})


@receiver(pre_save, sender=Category)
def category_pre_save_reciever(sender, instance, ** kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class ProductManager(models.Manager):
    def all(self):
        return self.get_queryset().filter(is_active=True)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=50, default='Anonymous')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    slug = models.SlugField(unique=True, blank=True)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})


@receiver(pre_save, sender=Product)
def product_pre_save_reciever(sender, instance, ** kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

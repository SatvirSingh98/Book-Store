from random import choice
from string import ascii_letters, digits

from django.utils.text import slugify


def random_string_generator(size=10, chars=ascii_letters+digits):
    return ''.join(choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        try:
            slug = slugify(instance.name)
        except Exception:
            slug = slugify(instance.title)

    klass = instance.__class__
    qs = klass.objects.filter(slug=slug)
    if qs.exists():
        new_slug = '{slug}-{randstr}'.format(
            slug=slug,
            randstr=random_string_generator(size=5)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

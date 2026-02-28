from django.contrib.auth.hashers import make_password
from django.db import migrations


CATEGORIES = [
    ('Electronics', 'electronics'),
    ('Clothing', 'clothing'),
    ('Books', 'books'),
    ('Food & Beverages', 'food-beverages'),
    ('Sports', 'sports'),
    ('Home & Garden', 'home-garden'),
]


def seed_data(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    for name, slug in CATEGORIES:
        Category.objects.create(name=name, slug=slug)

    User = apps.get_model('auth', 'User')
    User.objects.create(
        username='admin',
        password=make_password('password'),
        email='admin@example.com',
        is_staff=True,
        is_superuser=True,
        is_active=True,
    )


def unseed_data(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Category.objects.filter(slug__in=[slug for _, slug in CATEGORIES]).delete()

    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_code=unseed_data),
    ]

from django.db import migrations


TAGS = [
    ('New Arrival', 'new-arrival'),
    ('Best Seller', 'best-seller'),
    ('Sale', 'sale'),
    ('Featured', 'featured'),
    ('Limited Edition', 'limited-edition'),
    ('Eco-Friendly', 'eco-friendly'),
    ('Organic', 'organic'),
    ('Handmade', 'handmade'),
    ('Premium', 'premium'),
    ('Budget-Friendly', 'budget-friendly'),
]


def seed_tags(apps, schema_editor):
    Tag = apps.get_model('store', 'Tag')
    Tag.objects.bulk_create([Tag(name=name, slug=slug) for name, slug in TAGS])


def unseed_tags(apps, schema_editor):
    Tag = apps.get_model('store', 'Tag')
    Tag.objects.filter(slug__in=[slug for _, slug in TAGS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_tag_product_tags'),
    ]

    operations = [
        migrations.RunPython(seed_tags, reverse_code=unseed_tags),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_seed_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_available',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/'),
        ),
    ]

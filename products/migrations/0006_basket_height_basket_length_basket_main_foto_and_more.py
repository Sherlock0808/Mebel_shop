# Generated by Django 5.1.1 on 2024-09-09 20:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_productimage_image_alter_products_main_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='height',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AddField(
            model_name='basket',
            name='length',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AddField(
            model_name='basket',
            name='main_foto',
            field=models.ImageField(blank=True, null=True, upload_to='main_product_images'),
        ),
        migrations.AddField(
            model_name='basket',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basket',
            name='product_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basket',
            name='width',
            field=models.CharField(default=0, max_length=20),
        ),
    ]

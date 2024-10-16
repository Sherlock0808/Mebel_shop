# Generated by Django 5.1.1 on 2024-09-11 09:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_basket_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='favouriteproducts',
            name='category',
            field=models.CharField(default=django.utils.timezone.now, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='favouriteproducts',
            name='height',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AddField(
            model_name='favouriteproducts',
            name='length',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AddField(
            model_name='favouriteproducts',
            name='main_foto',
            field=models.ImageField(blank=True, null=True, upload_to='main_product_images'),
        ),
        migrations.AddField(
            model_name='favouriteproducts',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='favouriteproducts',
            name='product_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='favouriteproducts',
            name='width',
            field=models.CharField(default=0, max_length=20),
        ),
    ]

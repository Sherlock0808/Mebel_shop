# Generated by Django 5.1.1 on 2024-09-28 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_favouriteproducts_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favouriteproducts',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.categories'),
        ),
    ]

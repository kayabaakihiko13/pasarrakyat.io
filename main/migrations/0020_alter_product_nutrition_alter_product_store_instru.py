# Generated by Django 4.1 on 2022-08-06 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_remove_productattribute_image_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='nutrition',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='store_instru',
            field=models.TextField(max_length=400),
        ),
    ]

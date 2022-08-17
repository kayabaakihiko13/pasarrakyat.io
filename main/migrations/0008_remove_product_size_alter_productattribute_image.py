# Generated by Django 4.0.6 on 2022-08-02 03:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_product_brand_remove_productattribute_brand_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='product_imgs/'),
            preserve_default=False,
        ),
    ]
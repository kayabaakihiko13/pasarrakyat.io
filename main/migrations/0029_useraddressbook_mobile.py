# Generated by Django 3.2 on 2022-08-18 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20220818_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddressbook',
            name='mobile',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

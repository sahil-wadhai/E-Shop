# Generated by Django 4.1.7 on 2023-11-01 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_address_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='mobile',
        ),
    ]

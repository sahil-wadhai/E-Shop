# Generated by Django 4.1.7 on 2023-11-01 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='mobile',
            field=models.CharField(default='', max_length=10),
        ),
    ]

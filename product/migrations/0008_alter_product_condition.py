# Generated by Django 4.1.7 on 2023-11-05 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_product_pickup_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('new', 'New'), ('used', 'Used')], default='new', max_length=10),
        ),
    ]

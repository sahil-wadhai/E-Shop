# Generated by Django 4.1.7 on 2023-11-01 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_delivery_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.payment'),
        ),
    ]

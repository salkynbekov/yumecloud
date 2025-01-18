# Generated by Django 5.1.5 on 2025-01-18 14:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_rental', models.DateField(verbose_name='Начало аренды')),
                ('end_rental', models.DateField(verbose_name='Конец аренды')),
                ('total_price', models.DecimalField(decimal_places=2, default=None, max_digits=10, verbose_name='Общая стоимость')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название продукта')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена продукта')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена продукта в аренде')),
                ('duration', models.PositiveIntegerField(verbose_name='Продолжительность аренды')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='rental.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='rental.product', verbose_name='Продукт')),
            ],
            options={
                'unique_together': {('order', 'product')},
            },
        ),
    ]

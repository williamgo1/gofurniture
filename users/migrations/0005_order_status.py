# Generated by Django 5.1.6 on 2025-03-16 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_orderitem_price_remove_orderitem_product_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('active', 'Активный'), ('completed', 'Завершенный'), ('cancelled', 'Отмененный')], default='active', max_length=10, verbose_name='Статус заказа'),
        ),
    ]

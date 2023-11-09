# Generated by Django 4.2.7 on 2023-11-09 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_order_date_order_overall'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='wishlistitem',
            options={'verbose_name': 'Желаемый товар пользователя', 'verbose_name_plural': 'Желаемые товары пользователей'},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='date',
            new_name='creation_date',
        ),
    ]
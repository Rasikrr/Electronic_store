# Generated by Django 4.2.7 on 2023-11-11 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField()),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('order_status', models.CharField(choices=[('created', 'Created'), ('canceled', 'Canceled'), ('in transit', 'In transit'), ('delivered', 'delivered')], default='Created', max_length=50)),
                ('cart_items', models.ManyToManyField(to='core.cartitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderCartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cartitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order')),
            ],
        ),
    ]
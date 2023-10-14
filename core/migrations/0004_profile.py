# Generated by Django 4.2.6 on 2023-10-14 20:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_customuser_password_2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 3.1 on 2021-08-19 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20210819_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampark_sevekari',
            name='User_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]

# Generated by Django 3.1 on 2021-08-17 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sscode',
            field=models.CharField(max_length=5),
        ),
    ]

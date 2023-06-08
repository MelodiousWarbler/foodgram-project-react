# Generated by Django 2.2.28 on 2023-06-07 17:32

from django.db import migrations, models

import foodgram.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[foodgram.validators.validate_username], verbose_name='Уникальный юзернейм'),
        ),
    ]

# Generated by Django 4.0.6 on 2022-07-27 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='telegramuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'Users'},
        ),
    ]

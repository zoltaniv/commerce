# Generated by Django 4.2 on 2023-04-13 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rate_start_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='start_rate',
        ),
    ]
# Generated by Django 4.2 on 2023-04-13 19:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_auction_image_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='start_rate',
            field=models.IntegerField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

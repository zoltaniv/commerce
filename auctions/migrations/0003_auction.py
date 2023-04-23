# Generated by Django 4.2 on 2023-04-10 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lot', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=256)),
                ('first_rate', models.IntegerField()),
                ('image', models.FileField(upload_to='auctions/images')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='auctions.category')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

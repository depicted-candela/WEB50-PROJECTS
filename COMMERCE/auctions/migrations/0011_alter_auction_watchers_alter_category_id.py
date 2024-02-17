# Generated by Django 4.1.6 on 2023-02-17 20:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_auction_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='auctions_watchers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
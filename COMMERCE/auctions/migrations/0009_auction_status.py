# Generated by Django 4.1.6 on 2023-02-14 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_product_bid_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
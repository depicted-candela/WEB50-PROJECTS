# Generated by Django 4.1.6 on 2023-02-13 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_auction_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='product',
            new_name='auction',
        ),
    ]

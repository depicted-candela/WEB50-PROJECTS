# Generated by Django 4.1.6 on 2023-03-26 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_post_options_post_likes_alter_post_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=1),
        ),
    ]
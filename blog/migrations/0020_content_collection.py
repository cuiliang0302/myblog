# Generated by Django 3.1.3 on 2020-11-27 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_auto_20201123_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='collection',
            field=models.PositiveIntegerField(default=0, verbose_name='收藏数'),
        ),
    ]

# Generated by Django 3.1.1 on 2020-11-10 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0012_auto_20201109_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='describe',
            field=models.CharField(default='', max_length=100, verbose_name='图片标题'),
        ),
    ]

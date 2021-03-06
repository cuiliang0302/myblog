# Generated by Django 3.1.1 on 2020-10-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_bloggerinfo_websiteconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='websiteconfig',
            name='copyright',
            field=models.CharField(max_length=10, verbose_name='版权信息'),
        ),
        migrations.AlterField(
            model_name='websiteconfig',
            name='descript',
            field=models.CharField(max_length=300, verbose_name='META描述'),
        ),
        migrations.AlterField(
            model_name='websiteconfig',
            name='index_title',
            field=models.CharField(max_length=50, verbose_name='首页标题'),
        ),
        migrations.AlterField(
            model_name='websiteconfig',
            name='keywords',
            field=models.CharField(max_length=200, verbose_name='META关键词'),
        ),
    ]

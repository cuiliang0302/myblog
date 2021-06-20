# Generated by Django 3.1.3 on 2020-11-22 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20201122_1340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catalogue',
            options={'verbose_name': '笔记目录', 'verbose_name_plural': '笔记目录'},
        ),
        migrations.AlterModelOptions(
            name='note',
            options={'verbose_name': '笔记名称', 'verbose_name_plural': '笔记名称'},
        ),
        migrations.AlterField(
            model_name='catalogue',
            name='father',
            field=models.IntegerField(blank=True, null=True, verbose_name='父目录ID'),
        ),
    ]
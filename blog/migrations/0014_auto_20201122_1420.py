# Generated by Django 3.1.3 on 2020-11-22 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20201122_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogue',
            name='is_unfold',
        ),
        migrations.AlterField(
            model_name='catalogue',
            name='order',
            field=models.IntegerField(verbose_name='序号'),
        ),
    ]
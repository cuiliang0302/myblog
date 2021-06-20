# Generated by Django 3.1.3 on 2020-12-20 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20201219_1601'),
        ('account', '0025_auto_20201219_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleviewhistory',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='所属分类'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='phone',
            field=models.CharField(default='保密', max_length=20, verbose_name='手机号'),
        ),
    ]

# Generated by Django 3.1.1 on 2020-09-29 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200929_0958'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leavemessage',
            options={'ordering': ('root_id', 'level'), 'verbose_name': '留言记录表', 'verbose_name_plural': '留言记录表'},
        ),
        migrations.AddField(
            model_name='leavemessage',
            name='root_id',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='根留言ID'),
        ),
    ]

# Generated by Django 3.1.1 on 2020-09-29 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20200929_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leavemessage',
            name='comment_img',
        ),
    ]

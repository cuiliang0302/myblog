# Generated by Django 3.1.1 on 2020-09-29 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_leavemessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leavemessage',
            name='father',
        ),
        migrations.AddField(
            model_name='leavemessage',
            name='like',
            field=models.IntegerField(default=0, verbose_name='留言点赞数'),
        ),
        migrations.AddField(
            model_name='leavemessage',
            name='reply_id',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='回复留言ID'),
        ),
    ]
# Generated by Django 3.1.1 on 2020-09-29 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20200929_1109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leavemessage',
            options={'ordering': ('root_id', 'level', '-time'), 'verbose_name': '留言记录表', 'verbose_name_plural': '留言记录表'},
        ),
        migrations.AddField(
            model_name='leavemessage',
            name='comment_img',
            field=models.ImageField(blank=True, null=True, upload_to='comment/', verbose_name='头像'),
        ),
    ]

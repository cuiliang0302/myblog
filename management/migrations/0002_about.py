# Generated by Django 3.1.1 on 2020-09-30 22:54

from django.db import migrations, models
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', mdeditor.fields.MDTextField()),
            ],
            options={
                'verbose_name': '关于',
                'verbose_name_plural': '关于',
            },
        ),
    ]

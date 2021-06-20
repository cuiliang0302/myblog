# Generated by Django 3.1.3 on 2020-11-23 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_remove_note_is_release'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='content',
        ),
        migrations.AddField(
            model_name='content',
            name='note',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.note', verbose_name='所属笔记'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.1.3 on 2020-12-02 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0020_content_collection'),
        ('account', '0020_remove_articleviewhistory_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentmessage',
            options={'ordering': ('root_id', 'level', '-time'), 'verbose_name': '博文评论回复记录', 'verbose_name_plural': '博文评论回复记录'},
        ),
        migrations.RemoveField(
            model_name='contentviewhistory',
            name='note',
        ),
        migrations.CreateModel(
            name='NoteMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True, verbose_name='评论内容')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('level', models.IntegerField(default=0, verbose_name='评论等级')),
                ('like', models.IntegerField(default=0, verbose_name='评论点赞数')),
                ('reply_id', models.IntegerField(blank=True, default=None, null=True, verbose_name='回复评论ID')),
                ('root_id', models.IntegerField(blank=True, default=None, null=True, verbose_name='回复根ID')),
                ('note', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.content', verbose_name='笔记')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名')),
            ],
            options={
                'verbose_name': '笔记评论回复记录',
                'verbose_name_plural': '笔记评论回复记录',
                'ordering': ('root_id', 'level', '-time'),
            },
        ),
    ]

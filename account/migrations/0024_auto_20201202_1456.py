# Generated by Django 3.1.3 on 2020-12-02 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0021_auto_20201202_1352'),
        ('account', '0023_auto_20201202_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionViewHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='浏览时间')),
                ('is_like', models.BooleanField(default=0, verbose_name='是否收藏')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.section', verbose_name='笔记标题')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名')),
            ],
            options={
                'verbose_name': '笔记浏览记录',
                'verbose_name_plural': '笔记浏览记录',
                'ordering': ('-time',),
            },
        ),
        migrations.DeleteModel(
            name='ContentViewHistory',
        ),
    ]

# Generated by Django 3.1.1 on 2020-10-21 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_about_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloggerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=10, verbose_name='职位')),
                ('company', models.CharField(max_length=20, verbose_name='单位')),
                ('location', models.CharField(max_length=10, verbose_name='地址')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('csdn', models.URLField(max_length=50, verbose_name='CSDN')),
                ('github', models.URLField(max_length=50, verbose_name='GitHub')),
            ],
            options={
                'verbose_name': '博主信息',
                'verbose_name_plural': '博主信息',
            },
        ),
        migrations.CreateModel(
            name='WebsiteConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='网站名称')),
                ('domain', models.URLField(max_length=50, verbose_name='网站域名')),
                ('index_title', models.CharField(max_length=20, verbose_name='首页标题')),
                ('keywords', models.CharField(max_length=100, verbose_name='META关键词')),
                ('descript', models.CharField(max_length=200, verbose_name='META描述')),
                ('copyright', models.CharField(max_length=50, verbose_name='版权信息')),
            ],
            options={
                'verbose_name': '网站配置',
                'verbose_name_plural': '网站配置',
            },
        ),
    ]

# Generated by Django 3.1.3 on 2020-11-22 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20201122_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='FirstCatalogue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('order', models.IntegerField(verbose_name='序号')),
                ('note', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.note', verbose_name='笔记名称')),
            ],
            options={
                'verbose_name': '笔记一级目录',
                'verbose_name_plural': '笔记一级目录',
            },
        ),
        migrations.CreateModel(
            name='SecondCatalogue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(verbose_name='序号')),
                ('content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.content', verbose_name='笔记名称')),
                ('father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.firstcatalogue', verbose_name='一级目录名称')),
            ],
            options={
                'verbose_name': '笔记二级目录',
                'verbose_name_plural': '笔记二级目录',
            },
        ),
        migrations.DeleteModel(
            name='Catalogue',
        ),
    ]

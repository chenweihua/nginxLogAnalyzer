# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_overall_scripttime'),
    ]

    operations = [
        migrations.CreateModel(
            name='regex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regex', models.CharField(db_index=True, max_length=225, null=True)),
                ('status', models.CharField(db_index=True, default='not done', max_length=225, null=True)),
            ],
        ),
    ]
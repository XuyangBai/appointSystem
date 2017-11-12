# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-11 11:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0031_auto_20171110_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.Classroom'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='custom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
    ]

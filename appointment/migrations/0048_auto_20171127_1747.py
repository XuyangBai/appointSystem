# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-27 09:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20171121_1048'),
        ('classroom', '0002_classroom_location'),
        ('appointment', '0047_auto_20171122_1130'),
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
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together=set([('custom', 'classroom', 'date', 'end', 'status'), ('custom', 'classroom', 'date', 'start', 'status')]),
        ),
    ]

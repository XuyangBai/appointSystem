# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-11 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0013_auto_20171111_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='major',
            field=models.CharField(choices=[('EE', '\u7535\u5b50'), ('CS', '\u8ba1\u7b97\u673a'),
                                            ('CST', '\u8ba1\u7b97\u673a\u5e08\u8303')], default='EE', max_length=10),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-20 21:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0015_auto_20170417_1744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transition',
            old_name='static_args',
            new_name='permanent_tokens',
        ),
    ]

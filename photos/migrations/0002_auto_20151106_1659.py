# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photouser',
            name='auth_token',
            field=models.CharField(max_length=128, default='x'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photouser',
            name='vk_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='photouser',
            name='vk_key',
            field=models.CharField(max_length=128, blank=True, null=True),
        ),
    ]

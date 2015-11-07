# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='photouser',
            name='status',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='photouser',
            name='vk_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]

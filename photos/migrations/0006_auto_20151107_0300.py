# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0005_auto_20151107_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='photouser',
            name='avatar',
            field=models.ImageField(null=True, upload_to='ava/', blank=True),
        ),
        migrations.AddField(
            model_name='photouser',
            name='thumb',
            field=models.ImageField(null=True, upload_to='ava/thumb/', blank=True),
        ),
    ]

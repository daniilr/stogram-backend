# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_auto_20151107_0218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photouser',
            old_name='vk_url',
            new_name='url',
        ),
    ]

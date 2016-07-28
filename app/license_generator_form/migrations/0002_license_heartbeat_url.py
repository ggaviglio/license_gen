# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license_generator_form', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='heartbeat_url',
            field=models.TextField(default=''),
        ),
    ]

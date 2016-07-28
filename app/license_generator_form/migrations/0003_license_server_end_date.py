# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license_generator_form', '0002_license_heartbeat_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='server_end_date',
            field=models.TextField(default=''),
        ),
    ]

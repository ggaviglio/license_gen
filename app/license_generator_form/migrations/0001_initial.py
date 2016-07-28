# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('release_key', models.TextField(default='')),
                ('notes', models.TextField(default='')),
                ('external_id', models.TextField(default='')),
                ('external_id_type', models.TextField(default='')),
                ('license_type', models.TextField(default='')),
                ('account_holder', models.TextField(default='')),
                ('expiry_days', models.IntegerField(null=True)),
                ('max_users', models.IntegerField(null=True)),
                ('no_heartbeat', models.BooleanField(default=False)),
                ('clustering_enabled', models.BooleanField(default=False)),
                ('license_group', models.TextField(default='')),
                ('expiry_date', models.TextField(default='')),
                ('max_docs', models.IntegerField(null=True)),
                ('cloud_sync', models.BooleanField(default=False)),
                ('crypto_doc', models.BooleanField(default=False)),
            ],
        ),
    ]

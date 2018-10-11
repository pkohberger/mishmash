# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('error_class', models.CharField(max_length=128)),
                ('thrown_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=190, null=True, blank=True)),
                ('server', models.CharField(max_length=190, null=True, blank=True)),
                ('error_trace', models.TextField(null=True, blank=True)),
                ('message', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MasterLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_type', models.CharField(max_length=128)),
                ('message', models.TextField(null=True, blank=True)),
                ('location', models.CharField(max_length=190, null=True, blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]

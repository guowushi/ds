# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-13 03:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vmm', '0003_remove_vms_vm_disks1'),
    ]

    operations = [
        migrations.AddField(
            model_name='vms',
            name='vm_id',
            field=models.AutoField( primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='vms',
            name='vm_uuid',
            field=models.CharField(max_length=50),
        ),
    ]

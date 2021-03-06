# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginreg', '0002_remove_user_confirmpw'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.TextField(max_length=45)),
                ('description', models.TextField(max_length=45)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(auto_now=True)),
                ('user_id', models.ManyToManyField(related_name='trips', to='loginreg.User')),
            ],
        ),
    ]

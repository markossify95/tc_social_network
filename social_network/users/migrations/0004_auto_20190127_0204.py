# Generated by Django 2.1.5 on 2019-01-27 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190127_0203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='networkuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='networkuser',
            name='last_name',
        ),
    ]
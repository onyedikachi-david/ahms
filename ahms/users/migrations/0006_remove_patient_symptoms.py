# Generated by Django 3.1.13 on 2021-07-23 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='symptoms',
        ),
    ]

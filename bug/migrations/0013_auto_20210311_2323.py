# Generated by Django 2.2.3 on 2021-03-11 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bug', '0012_auto_20210311_2321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='ticket_member',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='ticket_team',
        ),
    ]

# Generated by Django 2.2.3 on 2021-03-09 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug', '0003_delete_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=250)),
            ],
        ),
    ]

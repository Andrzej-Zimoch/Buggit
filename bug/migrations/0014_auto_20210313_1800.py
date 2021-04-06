# Generated by Django 2.2.3 on 2021-03-13 17:00

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('bug', '0013_auto_20210311_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_manager',
            field=models.ForeignKey(blank=True, default=None, limit_choices_to={'level': 'manager'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_manager', to='bug.Profile'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_deadline',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='manager',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='team', chained_model_field='team_manager', default=None, on_delete=django.db.models.deletion.CASCADE, related_name='p_manager', to='bug.Profile'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='assigned_member',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='assigned_team', chained_model_field='members', on_delete=django.db.models.deletion.CASCADE, to='bug.Profile'),
        ),
    ]

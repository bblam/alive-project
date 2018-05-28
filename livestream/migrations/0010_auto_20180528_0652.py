# Generated by Django 2.0.5 on 2018-05-28 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livestream', '0009_merge_20180525_0909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appeal',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='approvalrequest',
            name='is_approved',
        ),
        migrations.AddField(
            model_name='appeal',
            name='status',
            field=models.CharField(choices=[('INACTIVE', 'inactive'), ('ACTIVE', 'active'), ('COMPLETED', 'completed')], default='INACTIVE', max_length=9),
        ),
        migrations.AddField(
            model_name='approvalrequest',
            name='status',
            field=models.CharField(choices=[('p', 'pending'), ('r', 'rejected'), ('a', 'approved')], default='p', max_length=1),
        ),
    ]

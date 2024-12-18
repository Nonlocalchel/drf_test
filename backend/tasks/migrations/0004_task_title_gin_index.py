# Generated by Django 5.0.6 on 2024-11-08 12:30

import django.contrib.postgres.indexes
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0003_task_title_upper_index_task_title_hash_index_and_more'),
        ('users', '0006_remove_user_users_user_id_1cecd0_idx'),
    ]

    operations = [
        TrigramExtension(),
        migrations.AddIndex(
            model_name='task',
            index=django.contrib.postgres.indexes.GinIndex(fields=['title'], name='title_gin_index',
                                                           opclasses=['gin_trgm_ops']),
        ),
    ]

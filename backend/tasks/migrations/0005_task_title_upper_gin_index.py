# Generated by Django 5.0.6 on 2024-11-08 12:48

import django.contrib.postgres.indexes
import django.db.models.functions.text
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_task_title_gin_index'),
        ('users', '0006_remove_user_users_user_id_1cecd0_idx'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='task',
            index=django.contrib.postgres.indexes.GinIndex(django.contrib.postgres.indexes.OpClass(django.db.models.functions.text.Upper('title'), name='gin_trgm_ops'), name='title_upper_gin_index'),
        ),
    ]

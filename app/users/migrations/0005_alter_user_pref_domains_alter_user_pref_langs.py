# Generated by Django 5.2.3 on 2025-06-21 19:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_pref_domains_alter_user_pref_langs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pref_domains',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('mobile', 'Mobile Development'), ('docs', 'Documentation'), ('frontend', 'Frontend'), ('backend', 'Backend'), ('game_dev', 'Game Development')], max_length=20), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='user',
            name='pref_langs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('c#', 'C#'), ('python', 'Python'), ('js', 'JS'), ('go', 'Go'), ('java', 'Java')], max_length=20), blank=True, default=list, size=None),
        ),
    ]

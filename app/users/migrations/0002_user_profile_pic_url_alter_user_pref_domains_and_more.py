# Generated by Django 5.2.3 on 2025-06-21 17:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic_url',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='pref_domains',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('game_dev', 'Game Development'), ('backend', 'Backend'), ('frontend', 'Frontend'), ('mobile', 'Mobile Development'), ('docs', 'Documentation')], max_length=20), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='user',
            name='pref_langs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('c#', 'C#'), ('js', 'JS'), ('go', 'Go'), ('java', 'Java'), ('python', 'Python')], max_length=20), blank=True, default=list, size=None),
        ),
    ]

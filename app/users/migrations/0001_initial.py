# Generated by Django 5.2.3 on 2025-06-21 17:11

import django.contrib.postgres.fields
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('registered_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('pref_langs', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('js', 'JS'), ('python', 'Python'), ('java', 'Java'), ('c#', 'C#'), ('go', 'Go')], max_length=20), blank=True, default=list, size=None)),
                ('pref_domains', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('docs', 'Documentation'), ('mobile', 'Mobile Development'), ('game_dev', 'Game Development'), ('frontend', 'Frontend'), ('backend', 'Backend')], max_length=20), blank=True, default=list, size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

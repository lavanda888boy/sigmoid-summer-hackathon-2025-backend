from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField


class Repo(models.Model):
    name = models.CharField(max_length=128, blank=False, unique=True)
    url = models.TextField(blank=False)
    
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    
    langs = ArrayField(
        base_field=models.CharField(max_length=20, choices=User.PREF_LANGS_CHOICES),
        default=list,
        blank=True,
    )

    domains = ArrayField(
        base_field=models.CharField(max_length=20, choices=User.PREF_DOMAINS_CHOICES),
        default=list,
        blank=True,
    )

    good_first = models.BooleanField(default=False)

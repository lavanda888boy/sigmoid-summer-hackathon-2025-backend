from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
import string
import random


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username field is required")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, password, **extra_fields)
    
    def make_random_password(self) -> str:
        groups = {
            'numbers': string.digits,
            'uppercase': string.ascii_uppercase,
            'lowercase': string.ascii_lowercase,
            'special': '#@$'
        }

        # Step 1: Pick 3 out of 4 groups randomly
        selected_groups = random.sample(list(groups.values()), 3)

        # Step 2: Ensure at least one character from each selected group
        password_chars = [random.choice(group) for group in selected_groups]

        # Step 3: Fill the rest of the password with random characters from all valid groups
        all_allowed = ''.join(groups.values())
        while len(password_chars) < 8:
            password_chars.append(random.choice(all_allowed))

        # Step 4: Shuffle to avoid predictable group ordering
        random.shuffle(password_chars)

        return ''.join(password_chars)


class User(AbstractBaseUser):
    PREF_LANGS_CHOICES = {
        ('c#', 'C#'),
        ('python', 'Python'),
        ('java', 'Java'),
        ('js', 'JS'),
        ('go', 'Go'),
    }

    PREF_DOMAINS_CHOICES = {
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('game_dev', 'Game Development'),
        ('mobile', 'Mobile Development'),
        ('docs', 'Documentation'),
    }
    
    username = models.CharField(max_length=100, unique=True, blank=False)    
    registered_at = models.DateTimeField(default=timezone.now)

    pref_langs = ArrayField(
        base_field=models.CharField(max_length=20, choices=PREF_LANGS_CHOICES),
        default=list,
        blank=True,
    )

    pref_domains = ArrayField(
        base_field=models.CharField(max_length=20, choices=PREF_DOMAINS_CHOICES),
        default=list,
        blank=True,
    )

    objects = CustomUserManager()

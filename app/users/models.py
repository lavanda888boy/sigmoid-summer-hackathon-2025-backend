from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
import string
import random


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, profile_pic_url=None, **extra_fields):
        if not email:
            raise ValueError("The email field is required")
        if not username:
            raise ValueError("The username field is required")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, profile_pic_url=profile_pic_url, **extra_fields)
        if password is None:
            user.set_password(self.make_random_password())
        else:
            user.set_password(password)
        user.save(using=self._db)

        return user

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
    PREF_LANGS_CHOICES = [
        ('c#', 'C#'),
        ('python', 'Python'),
        ('java', 'Java'),
        ('javascript', 'JavaScript'),
        ('go', 'Go'),
        ('typescript', 'TypeScript'),
        ('ruby', 'Ruby'),
        ('shell', 'Shell'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('c++', 'C++'),
    ]

    PREF_DOMAINS_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('game_dev', 'Game Development'),
        ('mobile', 'Mobile Development'),
        ('devops', 'Devops'),
        ('docs', 'Documentation'),
    ]
    
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
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

    profile_pic_url = models.TextField(blank=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = CustomUserManager()

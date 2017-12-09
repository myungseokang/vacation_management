from __future__ import unicode_literals, absolute_import

import hashlib

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Create common User overriding _create_user
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create Super User overriding _create_user
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, name):
        return self.get(**({self.model.USERNAME_FIELD: name}))


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField('이름', max_length=64)
    email = models.EmailField('이메일 주소', unique=True)
    TEAM_CHOICES = (
        (0, '기타'),
        (1, 'IT'),
        (2, '학예'),
        (3, '마케팅'),
        (4, 'CS'),
        (5, '경영지원'),
        (6, '오퍼레이션'),
        (7, '세일즈'),
    )
    remain_date = models.PositiveIntegerField('남은 일수', default=0)
    team = models.PositiveSmallIntegerField('팀', choices=TEAM_CHOICES, default=0)
    is_team_leader = models.BooleanField('팀리더 여부', default=False)
    is_staff = models.BooleanField(
        '어드민 여부',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    joined_time = models.DateTimeField('가입일시', default=timezone.now)
    last_activity = models.DateTimeField('마지막 로그인 일시', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_name(self):
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'pk': self.id})

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.get_name()

    @property
    def hashed_email(self):
        return hashlib.md5(self.email.encode()).hexdigest() if self.email else ''

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs):
        # 중복 공백 및 양끝 공백 삭제
        self.name = ' '.join(str(self.name).split())
        super(User, self).save(*args, **kwargs)

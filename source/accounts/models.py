from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(upload_to='user_pic', null=True, blank=True, verbose_name='Аватар')
    objects = UserManager()

    # def __str__(self):
    #     return '%s' % self.pk

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


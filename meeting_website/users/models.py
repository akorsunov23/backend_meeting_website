import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from .manager import CustomUserManager
from .services import watermark_overlay


class User(AbstractUser):
    """Абстрактная модель User, добавляет в стандартную модель дополнительные поля."""
    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    )

    email = models.EmailField(unique=True, verbose_name='электронная почта')
    photo = models.ImageField(upload_to='users_foto/', verbose_name='фотография')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='пол')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """Строковое представление объекта модели."""
        return f'{self.first_name} - {self.email}'

    def save(self, *args, **kwargs):
        """Перед сохранением фото, накладываем на него водяной знак."""
        if self.photo:
            # обрабатываем изображение
            output = watermark_overlay(photo_user=self.photo)

            # Заменяем оригинальное изображение на обработанное
            self.photo = InMemoryUploadedFile(
                output,
                'ImageField',
                f'user {self.first_name} {self.last_name}_{datetime.datetime.now()}.jpg',  # Имя файла для сохранения
                'image/jpeg',
                output.tell(),
                None
            )
        if self.password:
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

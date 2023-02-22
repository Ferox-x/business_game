from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class BaseUserModel(models.Model):
    """Базовая модель пользователей."""

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    patronymic = models.CharField(max_length=150, blank=True)

    phone_number = PhoneNumberField(blank=True)

    def get_full_name(self):
        """Преобразует имя и фамилию в одну строку."""
        return f"{self.last_name} {self.first_name} {self.patronymic}"

    class Meta:
        """Мета класс."""

        abstract = True

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from services.auth_services.generate_tokens import AccessToken


class UserManager(BaseUserManager):
    """Менеджер пользователя, создает пользователя и суперпользователя."""

    # def create_superuser(self, email, password=None):
    #     """ Создает и возввращет пользователя с привилегиями суперадмина. """
    #     if password is None:
    #         raise TypeError('Superusers must have a password.')
    #
    #     user = self.create_user(email, password)
    #     user.role_id = 1
    #     user.is_active = True
    #     user.is_superuser = True
    #     user.is_staff = True
    #     user.save
    #
    #     return user


class AuthUser(AbstractBaseUser, PermissionsMixin):
    """Модель авторизированного пользователя."""

    email = models.EmailField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = True
    is_coordinator = False
    is_player = False

    role = models.ForeignKey("users.UserRole", on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = "email"

    @property
    def access_token(self):
        """Свойство хранящее значение access токена."""
        return AccessToken().generate_token(user_id=self.id, user_role_id=self.role_id)

    class Meta:
        """Мета класс."""

        db_table = "auth_user"
        verbose_name = "auth_user"
        verbose_name_plural = "auth_users"

from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.core.validators import validate_email


class CustomValidatorsMethods:
    """Класс описывающий методы валидации данных."""

    @staticmethod
    def is_password_validate(password: str) -> list:
        """Метод валидации пароля.

        :param password:
        :return:
        """
        errors = list()
        try:
            validate_password(password=password)
        except exceptions.ValidationError as e:
            errors.extend(list(e.messages))
        return errors

    @staticmethod
    def is_email_validate(email: str) -> list:
        """Метод валидации email.

        :param email:
        :return:
        """
        errors = list()
        try:
            validate_email(value=email)
        except exceptions.ValidationError as e:
            errors.extend([error for error in e.messages])
        return errors

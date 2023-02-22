from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status

from services.reset_password.reset_password import ResetPassword


class EmailSending:
    """Класс отправки сообщений."""

    DEFAULT_CONTENT = {
        "domain": "0.0.0.0:8000",
        "site_name": "Business Games",
        "protocol": "http",
    }
    TEMPLATE_PASSWORD_RESET = "email_spam/reset_password.html"

    @classmethod
    def send_email_reset_password(cls, email_to: str) -> tuple:
        """Функция отправки сообщения с ссылкой на смену пароля."""
        content_tuple = ResetPassword.generate_content_for_reset_password(email_to)
        if content_tuple[0]:
            default_cont = cls.DEFAULT_CONTENT | content_tuple[1]
            message_html = render_to_string(cls.TEMPLATE_PASSWORD_RESET, default_cont)
            send_mail(
                "Восстановление пароля",
                "Hello!",
                settings.EMAIL_HOST_USER,
                [email_to],
                fail_silently=True,
                html_message=message_html,
            )
            return {"message": "Message has been sent"}, status.HTTP_200_OK

        return {
            "message": "User with this email doesn't exist "
        }, status.HTTP_400_BAD_REQUEST

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from services.email_sending.send_email import EmailSending
from services.reset_password.reset_password import ResetPassword

from .renders import UserJSONRenderer
from .serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    RefreshSerializer,
    RegistrationCoordinatorSerializer,
    RegistrationPlayerSerializer,
)


class RegistrationAPIView(APIView):
    """Класс APIView для регистрации новых игроков.

    methods: POST
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationPlayerSerializer

    def post(self, request: Request):
        """POST метод, для регистрации игроков."""
        user = request.data.get("user", {})

        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class RegistrationCoordinatorAPIView(APIView):
    """Класс APIView для регистрации новых координаторов.

    methods: POST
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationCoordinatorSerializer

    def post(self, request: Request):
        """POST метод, для регистрации координаторов."""
        user = request.data.get("user", {})

        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """Класс APIView для аутентификации пользователей.

    methods: POST
    """

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request: Request):
        """POST метод, авторизация.

        Метод принимающий post запрос, достает из тела запроса,
        почту и пароль, проверяет ,и при успехе отправляет токены.
        :return {
            'email': ...,
            'access_token': ...,
            'refresh_token': ...,
        }.
        """
        user = request.data.get("user", {})

        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshAPIView(APIView):
    """Класс APIView для обновления JWT токенов.

    methods: POST
    """

    permission_classes = (AllowAny,)
    serializer_class = RefreshSerializer

    def post(self, request):
        """POST метод, обновление токенов.

        Метод принимающий post запрос, достает из тела запроса,
        refresh_token, проверяет наличие пользователя в бд,
        и при успехе отправляет токены.
        :return {
            'access_token': ...,
        }.
        """
        if request.data.get("refreshToken") is None:
            errors = ["Учетные данные для аутентификации не были предоставлены."]

            return Response(
                {"errors": errors},
                status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(APIView):
    """Класс APIView для отправки ссылки сброса пароля на почту.

    methods: POST.
    """

    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def post(self, request):
        """Отправка сообщения методом POST."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = EmailSending.send_email_reset_password(
            serializer.validated_data.get("email")
        )
        return Response(response[0], status=response[1])


class PasswordResetConfirmAPIView(APIView):
    """APIView для смены пароля по ссылке из почты."""

    serializer_class = PasswordResetConfirmSerializer

    def put(self, request, token):
        """Смена пароля пользователя по токену.

        :param request:
        :param token:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_password_changed = ResetPassword.reset_password_confirm(
            serializer.validated_data, token
        )
        if is_password_changed[0]:
            return Response(
                {"message": is_password_changed[1]}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"errors": is_password_changed[1]}, status=status.HTTP_400_BAD_REQUEST
            )


class PasswordChangeAPIView(APIView):
    """APIView для изменнеия пароля."""

    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        """Метод изменения пароля."""
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data.get("new_password"))
        request.user.save()
        return Response(
            {"message": "Пароль был успешно обновлен"}, status=status.HTTP_200_OK
        )


class TestView(APIView):
    """Класс APIView для тестирования.

    methods: GET
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Тестирование."""
        return Response(status=200)

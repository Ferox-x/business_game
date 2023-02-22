import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    """Класс для рендера данных пользователя для отправки."""

    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        """Метод отображения."""
        token = data.get("access_token", None)

        if token is not None and isinstance(token, bytes):
            data["access_token"] = token.decode("utf-8")

        return json.dumps(data)

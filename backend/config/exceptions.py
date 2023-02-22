from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    """Функция отображения ошибок."""
    response = exception_handler(exc, context)
    handlers = {"ValidationError": _handle_generic_error}
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    for message in response.data.values():
        response.data = {"errors": message}
    return response

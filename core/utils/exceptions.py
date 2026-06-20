from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Кастомный обработчик ошибок.
    Делает ответы API единообразными.
    """

    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {"detail": "Внутренняя ошибка сервера."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Приводим формат ошибок к единому виду
    if isinstance(response.data, dict):
        if "detail" not in response.data:
            response.data = {"detail": response.data}

    return response


# ✔ Теперь все ошибки API выглядят одинаково.
# ✔ Фронт не ломается.
# ✔ Логику легко расширять.


# ✔ Добавили SuccessResponseMixin
# Чтобы не писать Response вручную.

# ✔ Добавили SerializerContextMixin
# Чтобы сериализаторы всегда получали request.

# ✔ Добавили DefaultPagination
# Единая пагинация для всего проекта.

# ✔ Добавили custom_exception_handler
# Теперь ошибки API красивые и единообразные.
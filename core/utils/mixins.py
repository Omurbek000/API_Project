from rest_framework.response import Response
from rest_framework import status


class SuccessResponseMixin:
    """
    Миксин для красивых успешных ответов.
    Используется в actions, где нужно вернуть:
    { "detail": "Успешно выполнено" }
    """

    def success(self, message="Успешно выполнено.", status_code=status.HTTP_200_OK):
        return Response({"detail": message}, status=status_code)


class SerializerContextMixin:
    """
    Добавляет request в контекст сериализатора.
    DRF делает это не всегда корректно в кастомных методах.
    """

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

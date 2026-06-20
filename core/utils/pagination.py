from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """
    Стандартная пагинация для всего проекта.
    - page_size = 10
    - page_size_query_param = "page_size"
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# ✔ Теперь все списки в API будут одинаково пагинироваться.
# ✔ Фронту удобно.
# ✔ API предсказуем.
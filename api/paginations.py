from rest_framework import pagination


class CardsPagination(pagination.PageNumberPagination):
    """Обычная пагинация по 10 элементов"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

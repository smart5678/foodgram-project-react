from rest_framework.pagination import PageNumberPagination


class ResultsSetPagination(PageNumberPagination):
    """
    Паджинатор для рецептов
    Размр страницы берется из параметра запроса limit
    """
    page_size = 6
    page_size_query_param = 'limit'

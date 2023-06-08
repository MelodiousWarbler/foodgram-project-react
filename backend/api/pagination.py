from rest_framework.pagination import PageNumberPagination

from foodgram import const


class Paginator(PageNumberPagination):
    page_size = const.PAGE_SIZE
    page_size_query_param = 'limit'

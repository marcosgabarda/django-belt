from rest_framework import pagination



class StandardPageNumberPagination(pagination.PageNumberPagination):
    """Overwrite to add support to the 'page_size' param."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 300

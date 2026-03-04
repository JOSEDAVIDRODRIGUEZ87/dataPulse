from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"  # Permite al cliente configurar: ?page_size=50
    max_page_size = 100  # Seguridad para evitar que pidan 1,000,000 de registros

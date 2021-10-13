from rest_framework.pagination import PageNumberPagination


class PageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def get_page_size(self, request):
        self.page_size = super().get_page_size(request)
        if self.page_size is not None and self.page_size > 1000:
            self.page_size = 1000
        return self.page_size

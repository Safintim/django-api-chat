from collections import OrderedDict

from rest_framework import pagination, response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data, custom_data=None, field='chat'):
        if custom_data is not None:
            return response.Response(OrderedDict([
                (field, custom_data),
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', data),
            ]))
        return response.Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))

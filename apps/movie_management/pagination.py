"""
custom pagination
"""
# python imports
import datetime
from collections import OrderedDict

# third party imports
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    """
    get_paginated_response: return OrderedDict with required attributes as last_page, next, previous links
    get_paginated_dict_response: return a dict object with the same values
    """

    def get_paginated_response(self, data):
        """
        :param data: queryset to be paginated
        :return: return a OrderedDict
        """
        return Response(OrderedDict([
            ('current', self.page.number),
            ('data', data),
            ('total_pages', self.page.paginator.num_pages),
            ('total', self.page.paginator.count),

        ]))

    def get_paginated_dict_response(self, data):
        """
        :param data: queryset to be paginated
        :return: return a simple dict obj
        """
        return {
            'current': self.page.number,
            'data': data,
            'total': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
        }


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    override LimitOffsetPagination
    """
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
            ('limit', self.get_limit(self.request)),
            ('offset', self.get_offset(self.request)),
            ('utc_time_now', datetime.datetime.now()),
        ]))


class CountryCustomLimitOffsetPagination(LimitOffsetPagination):
    """
    override LimitOffsetPagination
    """
    default_limit = 300

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
            ('limit', self.get_limit(self.request)),
            ('offset', self.get_offset(self.request)),
        ]))


def return_paginated_response(serializer_class, request, queryset):
    """
    used to return the paginated response
    """
    paginator = CustomLimitOffsetPagination()
    data = paginator.paginate_queryset(queryset, request)
    serializer = serializer_class(data, many=True)
    return paginator.get_paginated_response(serializer.data)

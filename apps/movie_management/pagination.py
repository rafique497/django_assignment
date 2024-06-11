"""
custom pagination
"""
# python imports
import datetime
from collections import OrderedDict

# third party imports
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


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



def return_paginated_response(serializer_class, request, queryset):
    """
    used to return the paginated response
    """
    paginator = CustomLimitOffsetPagination()
    data = paginator.paginate_queryset(queryset, request)
    serializer = serializer_class(data, many=True)
    return paginator.get_paginated_response(serializer.data)

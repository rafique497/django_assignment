"""
filters
"""
# django imports
from django.db.models import Q
from django_filters import rest_framework as filters

from apps.movie_management.models import Movie


class MovieListFilter(filters.FilterSet):
    """
    Filter objects.
    """
    search = filters.CharFilter()

    class Meta:
        """
        Meta class
        """
        model = Movie
        fields = ('search',)

    def filter_queryset(self, queryset):
        """
        used to search object based on title
        """
        search = self.data.get('search')

        search_query = Q()

        if search:
            search_query &= (Q(title__icontains=search))

        return queryset.filter(search_query).order_by('-id')

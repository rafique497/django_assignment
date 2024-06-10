"""
 urls file
"""
# third party imports
from rest_framework import routers

from apps.movie_management.views import MovieViewSet, ReviewViewSet

router = routers.SimpleRouter()

router.register('movie', MovieViewSet, basename='movie')
router.register('review', ReviewViewSet, basename='review')

urlpatterns = [
              ] + router.urls

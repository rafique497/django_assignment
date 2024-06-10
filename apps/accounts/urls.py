"""
 urls file
"""
# third party imports
from rest_framework import routers

from apps.accounts.views import RegisterViewSet

router = routers.SimpleRouter()

router.register('accounts', RegisterViewSet, basename='accounts')

urlpatterns = [
              ] + router.urls

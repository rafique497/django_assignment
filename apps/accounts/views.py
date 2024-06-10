"""
 view file
"""
# django import
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from apps.accounts.message import SUCCESS_CODE
# local import
from apps.accounts.models import User
from apps.accounts.serializers import (RegistrationSerializer, SigninSerializer)


class RegisterViewSet(GenericViewSet):
    """
    Registration view set
    """
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

    @action(methods=['post'], detail=False, url_path='register', url_name='register', permission_classes=[])
    def register(self, request, *args, **kwargs):
        """
        use to signup
        """
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': SUCCESS_CODE['2000']})

    @action(methods=['post'], detail=False, url_path='signin', url_name='signin',
            serializer_class=SigninSerializer, permission_classes=[])
    def signin(self, request, *args, **kwargs):
        """
        used for login
        """
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = user.get_token()
        return Response({'data': token})


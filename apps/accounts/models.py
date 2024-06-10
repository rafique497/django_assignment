from calendar import timegm
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User Model Class
    """
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    # here username_field is django defined field in account model, used for account identification.
    USERNAME_FIELD = 'email'

    # list of the field names that will be prompted for when creating a account via the
    # createsuperuser management command.
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return str(self.email)

    def generate_jwt_token(self, token_type: str, now_time: datetime, data: dict = dict, ):
        """
        used to generate jwt token
        """
        if type(data) == type:
            data = {}
        data.update({
            'token_type': token_type,
            'user_id': self.id,
            'email': self.email,
            'iss': 'your_site_url',
            'iat': datetime.utcnow(),
            'jti': uuid4().hex,
        })
        if token_type == 'refresh':
            exp = now_time + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        else:
            exp = now_time + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

        data.update({
            "exp": timegm(exp.utctimetuple())
        })
        token = jwt.encode(payload=data, key=settings.SIMPLE_JWT['SIGNING_KEY'],
                           algorithm=settings.SIMPLE_JWT['ALGORITHM'])

        return token

    def get_token(self, data: dict = dict):
        """get token"""
        now_time = datetime.utcnow()
        access = self.generate_jwt_token('access', now_time, data)
        refresh = self.generate_jwt_token('refresh', now_time, data)

        return {
            'access': access,
            'refresh': refresh
        }


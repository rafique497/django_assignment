"""
 serializer file
"""
from rest_framework import serializers

from apps.accounts.message import ERROR_CODE
from apps.accounts.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """
    used to serialize user objects
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    def validate(self, attrs):
        """ used to validate the incoming data """
        user = User.objects.filter(email__iexact=attrs['email']).first()
        if not user:
            return attrs

        if user.email and user.email.lower() == attrs['email'].lower():
            raise serializers.ValidationError({'message': ERROR_CODE['4000']})

    def create(self, validated_data):
        """ used to create user object"""
        user = User.objects.create(email=validated_data['email'],
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'],
                                   is_active=True
                                   )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SigninSerializer(serializers.ModelSerializer):
    """
    used to login user
    """

    email = serializers.EmailField(required=True, max_length=20)
    password = serializers.CharField(required=True, max_length=20)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        """ validate user object and user credential"""
        user = User.objects.filter(email__iexact=attrs['email']).first()

        if not user:
            raise serializers.ValidationError({'msg': ERROR_CODE['4001']})
        if not user.check_password(raw_password=attrs['password']):
            raise serializers.ValidationError({'msg': ERROR_CODE['4002']})
        attrs['user'] = user
        return attrs


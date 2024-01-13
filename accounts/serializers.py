from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name']
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

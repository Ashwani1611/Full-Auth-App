from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'mobile', 'address', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)   # 🔐 hash password
        user.save()

        return user


# class CustomTokenSerializer(TokenObtainPairSerializer):
#     username_field = 'email'

class ChangePasswordSerialiazer (serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

User = get_user_model()
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self , data):
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email is not exists")
        return data
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
#last commit


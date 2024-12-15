from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

CustomUser = get_user_model()  # Dynamically get the user model


class UserSerializer(serializers.ModelSerializer):
    # Explicitly define the password field with write-only property
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'password']

    def create(self, validated_data):
        # Use get_user_model().objects.create_user to create the user
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
        )
        # Automatically create a token for the newly created user
        Token.objects.create(user=user)
        return user

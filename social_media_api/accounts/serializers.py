from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import CustomUser  # Explicitly use your CustomUser model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'password']
    
    def create(self, validated_data):
        # Use CustomUser to create users
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
        )
        Token.objects.create(user=user)  # Create token here
        return user

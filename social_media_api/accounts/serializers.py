from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Write-only for security
    followers_count = serializers.SerializerMethodField()  # Custom field for count

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'followers_count', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'followers': {'read_only': True},  # Make followers read-only
        }

    def get_followers_count(self, obj):
        # Return the count of followers
        return obj.followers.count()

    def create(self, validated_data):
        # Ensure password is hashed during user creation
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
   

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']

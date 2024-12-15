from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser  # Import your CustomUser model
from .serializers import UserSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status, permissions


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Token creation handled in the serializer
            return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token = user.auth_token.key  # Token directly retrieved
            user_data = UserSerializer(user).data
            return Response({"token": token, "user": user_data}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class FollowViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """Follow a user."""
        try:
            user_to_follow = CustomUser.objects.get(pk=pk)
            if user_to_follow == request.user:
                return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            
            request.user.following.add(user_to_follow)
            return Response({"detail": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """Unfollow a user."""
        try:
            user_to_unfollow = CustomUser.objects.get(pk=pk)
            request.user.following.remove(user_to_unfollow)
            return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def followers(self, request):
        """Get a list of followers for the logged-in user."""
        followers = CustomUser.objects.filter(following=request.user)
        data = [{"id": follower.id, "username": follower.username} for follower in followers]
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def following(self, request):
        """Get a list of users the logged-in user is following."""
        following = request.user.following.all()
        data = [{"id": follow.id, "username": follow.username} for follow in following]
        return Response(data, status=status.HTTP_200_OK)




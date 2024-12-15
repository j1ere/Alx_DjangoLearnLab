from rest_framework import viewsets, permissions
from .models import Post, Comment,Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from rest_framework.views import APIView
from notifications.models import Notification
from rest_framework import status
from rest_framework import generics 

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(post=post, author=self.request.user)

    def get_post(self):
        post_id = self.kwargs['post_pk']
        return Post.objects.get(id=post_id)



class FeedView(APIView):
    """
    View to generate a feed of posts from users the current user follows.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the list of users the current user follows
        following_users = request.user.following.all()

        # Filter posts by authors in the following list and order by creation date
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        # Serialize the filtered posts
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Use generics.get_object_or_404 to fetch the Post
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # Generate a notification for the post author
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked",
                    target=post
                )
            return Response({"detail": "Post liked."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Use generics.get_object_or_404 to fetch the Post
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            like.delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from rest_framework.views import APIView

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
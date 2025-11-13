from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from blog.models import Post
from .serializers import PostSerializer

# Get , post , put , delete
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list(request):
    # posts = Post.objects.filter(published=True).order_by('-created_at')
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
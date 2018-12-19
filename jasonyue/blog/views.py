from rest_framework import generics
from blog.models import Post
from blog.serializers import PostSerializer
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
 
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class PostListCreate(generics.ListCreateAPIView):
    if ':1:blog' in cache:
        # get results from cache
        queryset = cache.get(':1:blog')
        serializer_class = PostSerializer

    else:
        queryset = Post.objects.all()
        serializer_class = PostSerializer
        cache.set('blog', queryset, timeout=CACHE_TTL)

def PostCreate(request, pk):
    if (':1:blog{}'.format(pk)) in cache:
        queryset = cache.get(':1:blog{}'.format(pk))
        serializer_class = PostSerializer(queryset)
        return JsonResponse(serializer_class.data)

    else:
        try:
            queryset = Post.objects.get(pk=pk)
            cache.set('blog{}'.format(pk), queryset, timeout=CACHE_TTL)
            serializer_class = PostSerializer(queryset)
            return JsonResponse(serializer_class.data)
        except Post.DoesNotExist:
            return HttpResponse(status=404)

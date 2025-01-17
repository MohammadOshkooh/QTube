# views.py
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import Video
from .serializers import VideoSerializer, CommentSerializer


class VideoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class VideoSearchView(ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Video.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))


class CommentView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CategoryListView(ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Video.objects.filter(category_id=category_id)

# views.py
from django.db.models import Q
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import Video, Category
from .serializers import VideoSerializer, CategorySerializer
from .tasks import convert_video_to_mp4


class VideoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            video = serializer.save(user=request.user)
            if not video.file.name.endswith('.mp4'):
                convert_video_to_mp4.delay(video.id)
            return Response({"message": "Video uploaded successfully. We are processing your video."}, status=201)
        return Response(serializer.errors, status=400)


class UserUploadedVideosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_videos = Video.objects.filter(user=request.user).order_by('-created_at')
        serializer = VideoSerializer(user_videos, many=True, context={'request': request})
        return Response(serializer.data, status=200)


class VideoSearchView(ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Video.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))


class GetVideoByCategoryAPIView(APIView):

    def post(self, request):
        videos = Video.objects.filter(processing_status="completed").all()

        category = request.data.get('category_id', None)
        if category:
            videos = videos.filter(category=category)

        serializer = VideoSerializer(videos, many=True).data

        return Response(serializer, status=200)


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class CreateCategory(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

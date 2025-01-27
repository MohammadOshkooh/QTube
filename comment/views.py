from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from comment.serializers import CommentSerializer
from qtube.models import Video


class CommentListView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            try:
                video_id = request.data.get('video_id')
            except Exception as e:
                return Response({"error": "video_id is required."}, status=status.HTTP_400_BAD_REQUEST)
            video = Video.objects.get(pk=video_id)
            comments = video.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=200)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        try:
            video = Video.objects.get(pk=video_id)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, video=video)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

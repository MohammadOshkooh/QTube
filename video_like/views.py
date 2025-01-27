from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from qtube.models import Video
from video_like.models import Like
from video_like.serializers import LikeSerializer


class LikeListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, video_id):
        """
        Retrieve all likes for a given video.
        """
        try:
            video = Video.objects.get(pk=video_id)
            likes = video.likes.all()
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)


class LikeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        """
        Add a like to a video by the authenticated user.
        """
        try:
            video = Video.objects.get(pk=video_id)

            # Check if the user has already liked this video
            if Like.objects.filter(video=video, user=request.user).exists():
                return Response({"error": "You have already liked this video."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new like
            like = Like.objects.create(video=video, user=request.user)
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)


class LikeDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can unlike a video

    def delete(self, request, video_id):
        """
        Remove a like from a video by the authenticated user.
        """
        try:
            video = Video.objects.get(pk=video_id)

            # Check if the user has liked this video
            like = Like.objects.filter(video=video, user=request.user).first()
            if not like:
                return Response({"error": "You have not liked this video."}, status=status.HTTP_400_BAD_REQUEST)

            # Delete the like
            like.delete()
            return Response({"message": "Like removed successfully."}, status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

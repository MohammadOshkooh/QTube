from celery import shared_task
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from .models import Video


@shared_task
def convert_video_to_mp4(video_id):
    try:
        video = Video.objects.get(id=video_id)
        video.processing_status = 'processing'
        video.save()

        input_file_path = video.file.path
        file_name, file_extension = os.path.splitext(input_file_path)

        print(file_name)
        print("==============")

        output_file_path = f"{file_name}.mp4"

        with VideoFileClip(input_file_path) as clip:
            clip.write_videofile(output_file_path, codec="libx264")

        video.file.name = file_name.replace('/code/back/media/', '') + ".mp4"
        video.processing_status = 'completed'
        video.save()

        if file_extension.lower() != ".mp4":
            os.remove(input_file_path)

    except Exception as e:
        print(f"Error converting video: {e}")

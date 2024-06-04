from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip
import numpy as np
import tempfile
import os
from .models import TextRequest


def generate_video(text):
    width, height = 100, 100
    duration = 3
    font_size = 20
    fps = 24

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, font_size)

    dummy_img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(dummy_img)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]


    def make_frame(t):
        img = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(img)

        x = width - int((t / duration) * (width + text_width))
        y = (height - text_height) // 2

        draw.text((x, y), text, font=font, fill='white')

        return np.array(img)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    video = VideoClip(make_frame, duration=duration)
    video.write_videofile(temp_file.name, fps=fps)
    return temp_file.name


def video_view(request):
    text = request.GET.get('text')

    text_request = TextRequest(text=text)
    text_request.save()

    video_path = generate_video(text)
    with open(video_path, 'rb') as video_file:
        response = HttpResponse(video_file.read(), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="scrolling_text.mp4"'
    os.remove(video_path)
    return response


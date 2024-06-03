from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip
import numpy as np


width, height = 100, 100
duration = 3
text = "Заходит как-то улитка в бар..."
font_size = 20
fps = 24

font = ImageFont.truetype("arial.ttf", font_size)

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

video = VideoClip(make_frame, duration=duration)
video.write_videofile("scrolling_text.mp4", fps=fps)

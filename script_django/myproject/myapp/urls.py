from django.urls import path
from .views import video_view

urlpatterns = [
    path('generate_video/', video_view, name='generate_video'),
]

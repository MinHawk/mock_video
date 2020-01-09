#coding:utf-8

from django.urls import path
from .views.base import Index
from .views.video import ExVideo, VideoSub, CusVideo

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('exvideo', ExVideo.as_view(), name='ex_video'),
    path('cusvideo', CusVideo.as_view(), name='cus_video'),
    path('subvideo/<int:video_id>', VideoSub.as_view(), name='sub_video')
]
#coding:utf-8

from django.urls import path
from .views.base import Index
from .views.auth import Login, LogoutAuth, AuthManager, UpdateAuthManager
from .views.video import (ExternalVideo, ExternalVideoSub,
                          ExternalVideoStar, StarRemove, VideoSubRemove, VideoUpdate,
                          VideoStatus)

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login', Login.as_view(), name='auth_login'),
    path('logout', LogoutAuth.as_view(), name='auth_logout'),
    path('auth/manager', AuthManager.as_view(), name='auth_manager'),
    path('auth/update', UpdateAuthManager.as_view(), name='update'),
    path('video/external_video', ExternalVideo.as_view(), name='external_video'),
    path('video/external_video/video_sub/<int:video_id>',
         ExternalVideoSub.as_view(),
         name='external_video_sub'
    ),
    path('video/external_video/video_star',
         ExternalVideoStar.as_view(),
         name='external_video_star'
    ),
    path('video/external_video/remove_star/<int:star_id>/<int:video_id>',
         StarRemove.as_view(),
         name='star_remove'
    ),
    path('video/external_video/remove_sub/<int:video_sub_id>/<int:video_id>',
         VideoSubRemove.as_view(),
         name='sub_remove'
    ),
    path('video/external_video/video_update/<int:video_id>',
         VideoUpdate.as_view(), name='video_update'
    ),
    path('video/external_video/video_status/<int:video_id>',
         VideoStatus.as_view(), name='video_status'
    )
]
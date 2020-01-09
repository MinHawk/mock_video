#coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse, get_object_or_404
from apps.libs.base_render import render_to_response
from apps.model.video import Video, FromTo

class ExVideo(View):

    TEMPLATE = 'client/video.html'

    def get(self, request):

        videos = Video.objects.exclude(from_to=FromTo.custom.value)

        data = {'videos': videos}

        return render_to_response(request, self.TEMPLATE, data=data)

class CusVideo(View):

    TEMPLATE = 'client/video.html'

    def get(self, request):

        videos = Video.objects.filter(from_to=FromTo.custom.value)

        data = {'videos': videos}

        return render_to_response(request, self.TEMPLATE, data=data)


class VideoSub(View):

    TEMPLATE = 'client/video_sub.html'

    def get(self, request, video_id):

        video = get_object_or_404(Video, pk=video_id)

        data = {'video': video}

        return render_to_response(request, self.TEMPLATE, data=data)
#coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse
from apps.libs.base_render import render_to_response
from apps.utils.permission import dashboard_auth
from apps.models import Video, VideoSub, VideoStar
from apps.utils.common import check_and_get_video_type, handle_video
from apps.model.video import VideoType, FromTo, NotionType


class ExternalVideo(View):

    TEMPLATE = 'dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):

        error = request.GET.get('error', '')
        data = {'error': error}

        cu_videos = Video.objects.filter(from_to=FromTo.custom.value)
        ex_videos = Video.objects.exclude(from_to=FromTo.custom.value)

        data['cu_video'] = cu_videos
        data['ex_video'] = ex_videos

        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):

        name = request.POST.get('name')
        image = request.POST.get('image')
        videotype = request.POST.get('videotype')
        fromto = request.POST.get('fromto')
        nation = request.POST.get('nation')
        videoinfo = request.POST.get('videoinfo')
        video_id = request.POST.get('video_id')

        if not all([name, image, videotype, fromto, nation, videoinfo]):
            return redirect('{}?error={}'.format(reverse('external_video'), '必填项不能为空'))

        if video_id:
            reverse_path = reverse('video_update', kwargs={'video_id': video_id})
        else:
            reverse_path = reverse('external_video')

        result = check_and_get_video_type(VideoType, videotype, '视频类型不存在')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse_path, result['msg']))
        # videotype_obj = result.get('data')

        result = check_and_get_video_type(FromTo, fromto, '视频来源不存在')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse_path, result['msg']))
        # fromto_obj = result.get('data')

        result = check_and_get_video_type(NotionType, nation, '视频类型不存在')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse_path, result['msg']))
        # nation_obj = result.get('data')

        print(video_id)
        if not video_id:
            try:
                Video.objects.create(
                    name=name,
                    image=image,
                    video_type=videotype,
                    from_to=fromto,
                    notions=nation,
                    info=videoinfo
                )
            except:
                return redirect('{}?error={}'.format(reverse_path, '创建失败'))
        else:
            try:
                video = Video.objects.get(pk=video_id)
                print(video)
                video.name = name
                video.image = image
                video.video_type = videotype
                video.from_to = fromto
                video.notions = nation
                video.info = videoinfo
                video.save()
            except:
                return redirect('{}?error={}'.format(reverse_path, '更新失败'))

        return redirect(reverse('external_video'))

class VideoUpdate(View):

    TEMPLATE = 'dashboard/video/video_update.html'

    @dashboard_auth
    def get(self, request, video_id):

        if video_id == 0:
            return render_to_response(request, self.TEMPLATE)

        video = Video.objects.get(pk=video_id)
        data = {'video': video}

        return render_to_response(request, self.TEMPLATE, data=data)

class ExternalVideoSub(View):

    TEMPLATE = 'dashboard/video/external_video_sub.html'

    @dashboard_auth
    def get(self, request, video_id):

        video = Video.objects.get(pk=video_id)

        data = {'video': video}

        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request, video_id):

        num = request.POST.get('number')
        video_sub_id = request.POST.get('video_sub_id')

        video = Video.objects.get(pk=video_id)

        if FromTo(video.from_to) == FromTo.custom:
            video_url = request.FILES.get('url')
        else:
            video_url = request.POST.get('url')

        # num = VideoSub.objects.count() + 1
        # num = video.video_sub.count() + 1

        if FromTo(video.from_to) == FromTo.custom:
            handle_video(video_url, video_id, num)
            print(video_url)
            return redirect(reverse('external_video_sub', kwargs={'video_id':video_id}))

        if not video_sub_id :
            try:
                VideoSub.objects.create(
                    video=video,
                    url=video_url,
                    number=num
                )
            except:
                return redirect(reverse('external_video_sub', kwargs={'video_id': video_id}))

        else:
            video_sub = VideoSub.objects.get(pk=video_sub_id)
            try:
                video_sub.number = num
                video_sub.url = video_url
                video_sub.save()
            except:
                return redirect(reverse('external_video_sub', kwargs={'video_id': video_id}))

        return redirect(reverse('external_video_sub', kwargs={'video_id':video_id}))


class StarRemove(View):

    def get(self, request, star_id, video_id):

        VideoStar.objects.filter(id=star_id).delete()

        return redirect(reverse('external_video_sub', kwargs={'video_id':video_id}))


class VideoSubRemove(View):

    def get(self, request, video_sub_id, video_id):

        VideoSub.objects.filter(id=video_sub_id).delete()

        return redirect(reverse('external_video_sub', kwargs={'video_id':video_id}))


class ExternalVideoStar(View):

    def post(self, request):

        star_name = request.POST.get('name')
        star_identity = request.POST.get('identity')
        video_id = request.POST.get('video_sub_id')

        video = Video.objects.get(pk=video_id)

        VideoStar.objects.create(
            video=video,
            name=star_name,
            identity=star_identity
        )

        return redirect(reverse('external_video_sub', kwargs={'video_id':video_id}))

class VideoStatus(View):

    def get(self, request, video_id):

        video = Video.objects.get(pk=video_id)

        video.status = not video.status

        video.save()

        return redirect(reverse('external_video'))
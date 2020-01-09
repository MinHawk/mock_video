#coding:utf-8

from enum import Enum
from django.db import models

class VideoType(Enum):
    movie = 'movie'
    cartoon = 'cartoon'
    episode = 'episode'
    variety = 'variety'
    other = 'other'

VideoType.movie.label = '电影'
VideoType.cartoon.label = '动漫'
VideoType.episode.label = '剧集'
VideoType.variety.label = '综艺'
VideoType.other.label = '其它'

class FromTo(Enum):
    youku = 'youku'
    iqiyi = 'iqiyi'
    tencent = 'tencent'
    custom = 'custom'

FromTo.youku.label = '优酷'
FromTo.iqiyi.label = '爱奇艺'
FromTo.tencent.label = '腾讯'
FromTo.custom.label = '自制'

class NotionType(Enum):
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    america = 'america'
    other = 'other'

NotionType.china.label = '中国'
NotionType.japan.label = '日本'
NotionType.korea.label = '韩国'
NotionType.america.label = '美国'
NotionType.other.label = '其它'

class RuleIdentity(Enum):
    star = 'star'
    support = 'support'
    director = 'director'
    screenwriter = 'screenwriter'

RuleIdentity.star.label = '主演'
RuleIdentity.support.label = '配角'
RuleIdentity.director.label = '导演'
RuleIdentity.screenwriter.label = '编剧'



class Video(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    from_to = models.CharField(max_length=20, null=False, default=FromTo.custom.value)
    notions = models.CharField(max_length=20, default=NotionType.other.value)
    info = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'video_type', 'from_to', 'notions')

    def __str__(self):
        return self.name

class VideoStar(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_star',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')

    @property
    def ident(self):
        try:
            result = RuleIdentity(self.identity)
        except:
            return ''
        return result.label

    class Meta:
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return self.name

class VideoSub(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_sub',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return 'video: {}, number: {}'.format(self.video.name, self.number)
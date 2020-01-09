#coding:utf-8

from mako.lookup import TemplateLookup
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse
from django.template.context import Context
import os

def render_to_response(request, template, data=None):

    #上下文请求实例化
    context_instance = RequestContext(request)
    #系统模板路径
    # path = settings.TEMPLATES[0]['DIRS'][0]
    path = os.path.join(settings.BASE_DIR, 'templates')

    #创建mako模板查找实例
    lookup = TemplateLookup(
        directories=[path],
        output_encoding='utf-8',
        input_encoding='utf-8'
    )

    #mako模板覆盖系统模板
    mako_template = lookup.get_template(template)

    #没有数据创建数据
    if not data:
        data = {}

    if context_instance:
        # 有请求到上下文实例，则将数据更新至实例
        context_instance.update(data)
    else:
        # 没有请求到上下实例，则创建上下文实例，并将数据传给上下文
        context_instance = Context(data)

    result = {}

    for d in context_instance:
        result.update(d)

    result['request'] = request
    result['csrf_token'] = ('<input type="hidden"'
                            ' name="csrfmiddlewaretoken" value={0}'
                            ' >'.format(request.META['CSRF_COOKIE']))

    return HttpResponse(mako_template.render(**result))
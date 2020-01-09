#coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse
from apps.libs.base_render import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator
from apps.utils.permission import dashboard_auth

class AuthManager(View):

    TEMPLATE = 'dashboard/auth/manage.html'

    @dashboard_auth
    def get(self, request):

        # if not request.user.is_authenticated:
        #     return redirect(reverse('auth_login'))

        users = User.objects.all()
        # users = User.objects.filter(is_superuser=True)

        page = request.GET.get('page', 1)

        p = Paginator(users, 2)
        current_page = p.get_page(page).object_list
        total_pagenu = p.num_pages

        if int(page) < 1:
            return redirect(reverse('auth_manager') + '?page=1')
            page = 1

        if int(page) > total_pagenu:
            return redirect(reverse('auth_manager') + '?page={}'.format(total_pagenu))
            page = total_pagenu

        data= {'users': current_page, 'total': total_pagenu, 'page_num': int(page)}

        return render_to_response(request, self.TEMPLATE, data=data)

class UpdateAuthManager(View):

    def get(self, request):

        status = request.GET.get('status', '')
        id = request.GET.get('id','')
        print(status, id)

        _status = True if status == 'on' else False

        user = User.objects.get(id=int(id))
        user.is_superuser = _status
        user.save()

        # request.user.is_superuser = _status
        # request.user.save()
        return redirect(reverse('auth_manager'))


class Login(View):

    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):

        if request.user.is_authenticated:
            return redirect(reverse('index'))

        to = request.GET.get('to', '')

        data = {'error': '', 'to': to}
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        to = request.GET.get('to')

        print(username, password)

        exist = User.objects.filter(username=username).exists()

        data = {}

        if not exist:
            data['error'] = '此用户不存在'
            return render_to_response(request, self.TEMPLATE, data=data)

        user = authenticate(username=username, password=password)

        if not user:
            data['error'] = '密码输入错误'
            return render_to_response(request, self.TEMPLATE, data=data)

        if not user.is_superuser:
            data['error'] = '您无权访问'
            return render_to_response(request, self.TEMPLATE, data=data)

        login(request, user)

        if to:
            return redirect(to)

        return redirect(reverse('index'))

class LogoutAuth(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('auth_login'))

#coding:utf-8

from django.views.generic import View
from apps.libs.base_render import render_to_response
from django.shortcuts import redirect, reverse

class Index(View):

    TEMPLATE = 'dashboard/index.html'

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect(reverse('auth_login'))

        return render_to_response(request, self.TEMPLATE)
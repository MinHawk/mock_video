#coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse

class Index(View):

    TEMPLATE = 'client/index.html'

    def get(self, request):
        return redirect(reverse('ex_video'))


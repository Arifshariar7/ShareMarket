# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# from .models import Theme

def home(request):
    # popular_themes = Theme.objects.filter(popular=True)
    context = {'popular_themes': ['magic formula']}
    return render(request, 'company/home.html', context)


def magic_formula(request):
    # stocks = Stock.objects.order_by('-mf_rank')
    return render(request, 'company/magic_formula.html', {})

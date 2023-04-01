# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from .models import Company,Yearly
from django.db.models import F,Subquery, OuterRef
from django.db.models.functions import Round,RowNumber



# from .models import Theme

def home(request):
    # popular_themes = Theme.objects.filter(popular=True)
    context = {'popular_themes': ['magic formula']}
    return render(request, 'company/home.html', context)


def magic_formula(request):
    # stocks = Stock.objects.order_by('-mf_rank')
    subquery = Yearly.objects.filter(company_id=OuterRef('pk')).order_by('id').values('npat')[:1]

    companies = Company.objects.all().annotate(
        ROE=Round(
            (Subquery(
                subquery
            ) / F('shareholders_equity')) * 100, 
            3
        )
    ).order_by('-ROE')

    score = 1
    for company in companies:
        company.score1 = score
        score += 1    
    return render(request, 'company/magic_formula.html', {'companies':companies})

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
    subquery= Yearly.objects.filter(company_id=OuterRef('pk')).order_by('id').values('npat')[:1]
    income_tax_query=Yearly.objects.filter(company_id=OuterRef('pk')).order_by('id').values('income_tax')[:1]
    interest_query=Yearly.objects.filter(company_id=OuterRef('pk')).order_by('id').values('interest')[:1]
    long_term_debt_query=Yearly.objects.filter(company_id=OuterRef('pk')).order_by('id').values('long_term_debt')[:1]
    short_term_debt_query=Yearly.objects.filter(company_id=OuterRef('pk')).order_by('id').values('short_term_debt')[:1]

    companies = Company.objects.all().annotate(
        ROE=Round(
            (Subquery(
                subquery
            ) / F('shareholders_equity')) * 100, 
            3
        )
    ).order_by('-ROE')

    
    companies = companies.annotate(
        ROCE=Round(
            (Subquery(
                subquery
            )+(income_tax_query)+(interest_query) / (F('shareholders_equity')+(long_term_debt_query)+(short_term_debt_query))) * 100, 
            3
        )
    ).order_by('-ROCE')
    companies.order_by('-ROE')
    score1 = 1
    for company in companies:
        company.score1 = score1
        score1 += 1   

    companies.order_by('-ROCE')

    score2 = 1
    for company in companies:
        company.score2 = score2
        score2 += 1    
    return render(request, 'company/magic_formula.html', {'companies':companies})

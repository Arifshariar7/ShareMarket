# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from .models import Company,Yearly, Daily
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
    cash_and_cash_eq = Yearly.objects.filter(company_id=OuterRef('pk')).order_by('id').values('cash_and_cash_eq')[:1]
    ltp = Daily.objects.filter(company_id=OuterRef('pk')).order_by('id').values('ltp')[:1]

    companies_list = []
    companies = Company.objects.all().annotate(
        ROE=Round(
            (Subquery(
                subquery
            ) / F('shareholders_equity')) * 100, 
            3
        )
    ).order_by('-ROE')

    score1 = 1
    for company in companies:
        company.score1 = score1
        companies_list.append(company)
        score1 += 1   
        
    companies = Company.objects.filter(id__in=[company.id for company in companies_list]).annotate(
        ROCE=Round(
            (((Subquery(
                subquery
            )+(income_tax_query)+(interest_query)) / ((F('shareholders_equity')+(long_term_debt_query)+(short_term_debt_query))))) * 100, 
            3
        )
    )

        # create a new list of companies and assign the score2 attribute
        # companies_list = []
    score2 = 1
    companies_list_final = []
    for company in companies:
        for c in companies_list:
            if c.id == company.id:
                company.score1 = c.score1
                company.ROE=c.ROE
        company.score2 = score2
        companies_list_final.append(company)
        score2 += 1
        # order by ROE and ROCE
    companies_list = companies_list_final
    companies = Company.objects.filter(id__in=[company.id for company in companies_list]).annotate(
    MARKET_CAP=Round(
        ( Subquery(ltp)) , 
        3
    )
).order_by('-MARKET_CAP')
    companies_list_final = []
    score3=1
    for company in companies:
        for c in companies_list:
            if c.id == company.id:
                company.score1 = c.score1
                company.score2 = c.score2
                company.ROE=c.ROE
                company.ROCE = c.ROCE
                company.MARKET_CAP *=company.total_share  
        company.score3 = score3
        companies_list_final.append(company)
        score3 += 1

    
        # order by ROE and ROCE
    companies_list = companies_list_final
    companies = Company.objects.filter(id__in=[company.id for company in companies_list]).annotate(
    Enterprise_Value=Round((
        Subquery(long_term_debt_query)+Subquery(short_term_debt_query))-Subquery(cash_and_cash_eq) , 
        3
    )
).order_by('-Enterprise_Value')
    companies_list_final = []
    score4=1
    for company in companies:
        for c in companies_list:
            if c.id == company.id:
                company.score1 = c.score1
                company.score2 = c.score2
                company.score3 = c.score3
                company.ROE=c.ROE
                company.ROCE = c.ROCE
                company.MARKET_CAP = c.MARKET_CAP
                company.Enterprise_Value+=company.MARKET_CAP
                company.Acquirer_Multiple = company.Enterprise_Value/(Yearly.objects.get(company=company.id).operating_profit)
                company.eps = 

        company.score4 = score4
        companies_list_final.append(company)
        score4+= 1



    companies = sorted(companies_list_final, key=lambda x: (x.score1+x.score2+x.score3+score4))

        # assign the final queryset to the list
        # companies = companies_list 
    return render(request, 'company/magic_formula.html', {'companies':companies})

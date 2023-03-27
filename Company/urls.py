from django.urls import re_path
from .views import home,magic_formula

app_name = 'Company'

urlpatterns = [
re_path('magic-formula/', magic_formula, name='magic_formula'),

    re_path('', home, name='home'),
]

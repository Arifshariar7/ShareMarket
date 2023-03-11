from django.contrib import admin
from .models import Company, Yearly, Daily, Quarter

admin.site.register(Company)
admin.site.register(Yearly)
admin.site.register(Daily)
admin.site.register(Quarter)
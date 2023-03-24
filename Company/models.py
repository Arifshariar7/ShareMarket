from django.db import models

class Company(models.Model):
    SECTOR_CHOICES = [
        ('Bank', 'Bank'),
        ('Cement', 'Cement'),
        ('Ceramics', 'Ceramics'),
        ('Corporate Bond', 'Corporate Bond'),
        ('Engineering', 'Engineering'),
        ('Financial Institusions', 'Financial Institusions'),
        ('Food and Allied', 'Food and Allied'),
        ('Fuel and Power', 'Fuel and Power'),
        ('Insurance', 'Insurance'),
        ('IT', 'IT'),
        ('Jute', 'Jute'),
        ('Life Insurance', 'Life Insurance'),
        ('Miscellaneous', 'Miscellaneous'),
        ('Mutual Funds', 'Mutual Funds'),
        ('Paper and Printing', 'Paper and Printing'),
        ('Pharmaceuticals and Chemicals', 'Pharmaceuticals and Chemicals'),
        ('Services and Real Estate', 'Services and Real Estate'),
        ('Tannery Industries', 'Tannery Industries'),
        ('Telecommunication', 'Telecommunication'),
        ('Textile', 'Textile'),
        ('Travel and Leisure', 'Travel and Leisure'),
    ]
    CATEGORY_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('N', 'N'),
        ('Z', 'Z'),
    ]
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    sectors = models.CharField(choices=SECTOR_CHOICES, max_length=70)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    total_share = models.FloatField()
    shareholders_equity = models.FloatField()
    def __str__(self) :
        return self.name

class Yearly(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='yearly_reports')
    timeline = models.DateTimeField()
    npat = models.FloatField()
    operating_profit = models.FloatField()
    income_tax = models.FloatField()
    interest = models.FloatField()
    long_term_debt = models.FloatField()
    short_term_debt = models.FloatField()
    cash_and_cash_eq = models.FloatField()
    eps = models.FloatField()

class Daily(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='daily_reports')
    timeline = models.DateTimeField()
    ltp = models.FloatField()

class Quarter(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='quarter_reports')
    quarter_name = models.CharField(max_length=255)
    eps_annual = models.FloatField()

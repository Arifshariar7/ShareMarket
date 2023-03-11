from django.db import models

class Company(models.Model):
    SECTOR_CHOICES = [
        ('TECH', 'Technology'),
        ('FIN', 'Finance'),
        ('CONS', 'Consumer'),
    ]
    CATEGORY_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    ]
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    sectors = models.CharField(choices=SECTOR_CHOICES, max_length=20)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    total_share = models.FloatField()
    shareholders_equity = models.FloatField()
    def __str__(self) -> str:
        return super().__str__(self.name)

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

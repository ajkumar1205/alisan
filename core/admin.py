from django.contrib import admin
from .models import Product, Lead, SiteVisit, SiteExpenses
# Register your models here.
admin.site.register(Product)
admin.site.register(Lead)
admin.site.register(SiteVisit)
admin.site.register(SiteExpenses)
from django.contrib import admin
from .models import Product, Lead, SiteVisit, SiteExpenses, Quotation
# Register your models here.
admin.site.register(Product)
admin.site.register(SiteVisit)
admin.site.register(SiteExpenses)

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superuser sees all leads
        elif request.user.role == 'admin' and request.user.franchise:
            return qs.filter(franchise=request.user.franchise)  # Franchise admin sees only their franchise leads
        return qs.none()  # For others, return no results

    list_display = ['name', 'phone_number', 'source', 'assigned_to']
    search_fields = ['name', 'phone_number']



@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superuser sees all quotations
        elif request.user.role == 'admin' and request.user.franchise:
            return qs.filter(lead__franchise=request.user.franchise)  # Franchise admin sees only their franchise quotations
        return qs.none()  # For others, return no results

    list_display = ['lead', 'total_amount', 'status', 'created_at']
    search_fields = ['lead__name']
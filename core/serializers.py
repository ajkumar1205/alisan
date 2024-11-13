from rest_framework import serializers
from .models import Lead, Product, SiteExpenses, SiteVisit, Quotation, Faq


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        exclude = ['created_by', 'assigned_to']


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        exclude = ['created_by', 'payments']


class SiteVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteVisit
        fields = '__all__'


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'
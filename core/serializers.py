from rest_framework import serializers
from .models import Lead, Product, SiteExpenses, SiteVisit


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



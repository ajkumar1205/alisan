from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Lead, Quotation, Faq
from .serializers import ProductSerializer, LeadSerializer, QuotationSerializer, FaqSerializer

from accounts.models import Employee


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter()


class LeadCreateView(GenericAPIView):
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        emp = Employee.objects.get(user=request.user)        

        serializer.save(created_by=emp)

        return Response("Lead created successfully", status=201)
    
    def get(self, request, *args, **kwargs):
        emp = Employee.objects.get(user=request.user)   
        leads = Lead.objects.filter(created_by=emp)
        return Response(LeadSerializer(leads, many=True).data)
    

class QuotationCreateView(GenericAPIView):
    serializer_class = QuotationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        emp = Employee.objects.get(user=request.user)        

        serializer.save(created_by=emp)

        return Response("Quotation created successfully", status=201)
    
    def get(self, request, *args, **kwargs):
        emp = Employee.objects.get(user=request.user)   
        leads = Quotation.objects.filter(created_by=emp)
        return Response(QuotationSerializer(leads, many=True).data)
    

class FaqListView(ListAPIView):
    serializer_class = FaqSerializer
    permission_classes = [IsAuthenticated]
    queryset = Faq.objects.all()


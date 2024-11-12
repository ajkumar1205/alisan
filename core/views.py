from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Lead
from .serializers import ProductSerializer, LeadSerializer

from accounts.models import Employee


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(franchise=user.franchise)


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
    


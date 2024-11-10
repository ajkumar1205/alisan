from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Lead
from .serializers import ProductSerializer, LeadSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()


class LeadCreateView(GenericAPIView):
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)

        return Response("Lead created successfully", status=201)
    
    def get(self, request, *args, **kwargs):
        leads = Lead.objects.filter(created_by=request.user)
        return Response(LeadSerializer(leads, many=True).data)
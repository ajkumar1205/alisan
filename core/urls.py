from django.urls import path
from .views import ProductListView, LeadCreateView, QuotationCreateView, FaqListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('leads/', LeadCreateView.as_view(), name='leads'),
    path('quotations/', QuotationCreateView.as_view(), name='quotations'),
    path('faqs/', FaqListView.as_view(), name='faqs'),
]

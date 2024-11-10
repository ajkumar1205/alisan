from django.urls import path
from .views import ProductListView, LeadCreateView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('leads/', LeadCreateView.as_view(), name='leads'),
]

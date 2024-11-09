from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('verify/', VerifyOtp.as_view(), name='verify'),
    path('employee/', EmployeeCreateView.as_view(), name='employee'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
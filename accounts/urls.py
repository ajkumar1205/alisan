from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('verify/', VerifyOtp.as_view(), name='verify'),
    path('employee/', EmployeeCreateView.as_view(), name='employee'),
    path('employee/neighbours/', NeighbourCreateView.as_view(), name='neighbours'),
    path('token/refresh/', CustomTokenObtainPairView.as_view(), name='token_refresh'),
    path('generate-url/', GeneratePresignedUrl.as_view(), name='presigned_url'),
]
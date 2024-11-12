from django.urls import path
from .views import AttendanceView, LeaveView

urlpatterns = [
    path('mark/', AttendanceView.as_view(), name='mark-attendance'),
    path('leave/', LeaveView.as_view(), name='apply-leave'),
]

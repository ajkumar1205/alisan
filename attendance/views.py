from django.forms import DateField
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import AttendanceSerializer, LeaveSerializer, HolidaySerializer
from .models import Holiday
from accounts.models import Employee
from .models import Leave


class AttendanceView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        emp = Employee.objects.get(user=request.user)
        serializer.save(employee=emp)

        return Response({'message': 'Attendance marked successfully!'})
    

class LeaveView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeaveSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        emp = Employee.objects.get(user=request.user)
        serializer.save(employee=emp)

        return Response({'message': 'Leave sent for approval!'})
    
    def get(self, request):
        emp = Employee.objects.get(user=request.user)
        leaves = Leave.objects.filter(employee=emp)
        serializer = self.get_serializer(leaves, many=True)
        return Response(serializer.data)
    
    

class HolidayView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HolidaySerializer
    
    
    def post(self, request):
        date = DateField(request.data['date'])
        holiday = Holiday.objects.filter(date=date).first()

        if holiday:
            return Response({'message': 'Holiday', 'description': holiday.description, "holiday": 1})
        
        emp = Employee.objects.get(user=request.user)

        # Check whether leave is applied or approved for the given date
        leave = Leave.objects.filter(employee=emp).first()

        if leave and leave.start_date <= date and leave.end_date >= date and leave.approved:
            return Response({'message': 'Leave', "holiday": 2})

        return Response({'message': 'Working Day', "holiday": 0})
    
    
    def get(self, request):
        holidays = Holiday.objects.all()
        serializer = self.get_serializer(holidays, many=True)
        return Response(serializer.data)
    

# SITE VISIT -> LOCATION SERVICE
# SITE VISIT -> ATTENDANCE MARKING
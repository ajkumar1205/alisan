from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import AttendanceSerializer, LeaveSerializer
from accounts.models import Employee


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
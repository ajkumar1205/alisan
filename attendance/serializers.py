from rest_framework import serializers
from .models import Attendance, Leave

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        exclude = ['employee']


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        exclude = ['employee', 'approved']
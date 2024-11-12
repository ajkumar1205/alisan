from rest_framework import serializers
from .models import Attendance, Leave, Holiday

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        exclude = ['employee']


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        exclude = ['employee', 'approved']


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'
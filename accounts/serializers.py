from rest_framework import serializers
from .models import MyUser, Employee, Neighbours

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['user', 'neighbours']
        

class NeighbourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighbours
        exclude = ['id']


class OtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        if not phone_number or not otp:
            raise serializers.ValidationError('Phone number and OTP is required')

        return data
    



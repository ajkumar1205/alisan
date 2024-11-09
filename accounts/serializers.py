from rest_framework import serializers
from .models import MyUser

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'phone_number', 'is_admin', 'is_staff', 'is_active']
        


class OtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        if not phone_number or not otp:
            raise serializers.ValidationError('Phone number and OTP is required')

        return data
    



from rest_framework import serializers
from .models import MyUser, Employee, Neighbours

from rest_framework import serializers

class NeighbourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighbours
        fields = [
            'first_name', 'first_phone',
            'second_name', 'second_phone',
            'third_name', 'third_phone'
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    # Add `neighbours_data` field for nested neighbor info
    neighbours_data = NeighbourSerializer(write_only=True)

    class Meta:
        model = Employee
        exclude = ['user', 'neighbours']

    def create(self, validated_data):
        neighbours_data = validated_data.pop('neighbours_data', None)

        neighbours_instance = None
        if neighbours_data:
            neighbours_instance = Neighbours.objects.create(**neighbours_data)
        
        employee = Employee.objects.create(neighbours=neighbours_instance, **validated_data)
        return employee

    def to_representation(self, instance):
        """Override to include neighbors' data in response"""
        representation = super().to_representation(instance)
        if instance.neighbours:
            representation['neighbours'] = NeighbourSerializer(instance.neighbours).data
        return representation



class OtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        if not phone_number or not otp:
            raise serializers.ValidationError('Phone number and OTP is required')

        return data
    



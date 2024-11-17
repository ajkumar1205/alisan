from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

import boto3
from botocore.exceptions import ClientError
import uuid

from .helpers import OtpHandler
from .serializers import OtpSerializer, EmployeeSerializer, NeighbourSerializer
from .models import Employee, MyUser


@api_view(['POST'])
def login(request):
    phone_number = request.data.get('phone_number')

    if not MyUser.objects.filter(phone_number=phone_number).exists():
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not phone_number:
        return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    otp_handler = OtpHandler(phone_number)

    if not otp_handler.send_otp():
        return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)


class VerifyOtp(GenericAPIView):
    serializer_class = OtpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        otp = serializer.validated_data.get('otp')

        otp_handler = OtpHandler(phone_number)

        if not otp_handler.verify_otp(otp):
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        User = get_user_model()
        user = User.objects.get(phone_number=phone_number)


        refresh = RefreshToken.for_user(user)

        if Employee.objects.filter(user=user).exists():
            emp = Employee.objects.get(user=user)
            return Response({
                'message': 'OTP verified successfully',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    'id': user.id,
                    'phone_number': user.phone_number,
                    'role': user.role,
                    'franchise': user.franchise
                },
                'employee': emp.id
            }, status=status.HTTP_200_OK)
        else: 
            return Response({
                'message': 'OTP verified successfully',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    'id': user.id,
                    'phone_number': user.phone_number,
                    'role': user.role,
                    'franchise': user.franchise
                },
                'employee': None
            }, status=status.HTTP_200_OK)
        


class GeneratePresignedUrl(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        file_name = f"{uuid.uuid4()}.jpg"

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        try:
            presigned_url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': file_name,
                    'ContentType': 'image/jpeg'
                },
                ExpiresIn=1800
            )
            return Response({'presigned_url': presigned_url, 'file_name': file_name}, status=status.HTTP_200_OK)
        except ClientError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class EmployeeCreateView(GenericAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        a_front = request.data.get('aadhar_front')
        a_back = request.data.get('aadhar_back')
        p_card = request.data.get('pan_card')
        d_license_front = request.data.get('driving_license_front')

        if not a_front or not a_back or not p_card or not d_license_front:
            return Response({"error": "aadhar_front, aadhar_back, pand_card and driving_license_front are required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the Employee with the authenticated user context
        serializer.save(
            user=user,
            aadhar_front = a_front,
            aadhar_back = a_back,
            pan_card = p_card,
            driving_license_front = d_license_front
        )
        
        return Response({'message': 'Employee created successfully'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        try:
            emp = Employee.objects.get(user=user)
            serializer = EmployeeSerializer(emp)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found for the user'}, status=status.HTTP_404_NOT_FOUND)
    

class NeighbourCreateView(GenericAPIView):
    serializer_class = NeighbourSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        n = serializer.save()

        try:
            emp = Employee.objects.get(user=user)
            emp.neighbours = n
            emp.save()
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found for the user'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Neighbour created and assigned successfully'}, status=status.HTTP_201_CREATED)
    


# Return Both Access and Refresh Token when the access token expires
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data['refresh'] = str(response.data['refresh'])
        response.data['access'] = str(response.data['access'])
        return response
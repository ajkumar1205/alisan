from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .helpers import OtpHandler
from .serializers import OtpSerializer


@api_view(['POST'])
def login(request):
    phone_number = request.data.get('phone_number')

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
        user = User.objects.filter(phone_number=phone_number).first()
        
        if not user:
            user = User.objects.create(phone_number=phone_number)
            user.set_password(otp_handler.set_password())
            user.save()
        
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'OTP verified successfully',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': {
                'id': user.id,
                'phone_number': user.phone_number,
            }
        }, status=status.HTTP_200_OK)
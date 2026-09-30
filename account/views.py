import random
from django.shortcuts import render
from .serializer import RegisterSerializer, LoginSerilaizer, ProfileSerializer, ResetPasswordSerializer, VerifyCodePasswordSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from account.serializer import UserUpdateSerializer
from account.models import OTPCode
from django.core.mail import send_mail
from project.settings import EMAIL_HOST_USER
from account.serializer import VarifyOTPCodeSerializer
from account.models import User

class Register(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            code = str(random.randint(100000, 999999))

            OTPCode.objects.filter(email=email).delete()

            OTPCode.objects.create(email=email, code=code)

            send_mail(
                subject='ваш код подверждения',
                message = f'Ваш код : {code}',
                from_email = EMAIL_HOST_USER,
                recipient_list = [email]
            )

            return Response({'message' : 'мы отправили код'})
        
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
            )
    


class Login(APIView):
    def post(self, request):
        serializer = LoginSerilaizer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            token, created = Token.objects.get_or_create(user = user)

            return Response({
                'message' : 'user was created with Token',
                'token' : token.key
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        

        
class ProfileAPIView(APIView):
    def get(self, request):

        serializer = ProfileSerializer(request.user)

        return Response(serializer.data)
    
    def patch(self, request):
        
        serializer = UserUpdateSerializer(request.user, data=request.data, partial = True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        


class VerifyCode(APIView):
    def post(self, request):
        serializer = VarifyOTPCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            otp = serializer.validated_data['otp']

            user = User.objects.create_user(
                email=email,
                username=email,
                password=password,
            )

            otp.delete()

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'User was created with token',
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)





class Resetpass(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            code = str(random.randint(100000, 999999))

            OTPCode.objects.filter(email=email).delete()

            OTPCode.objects.create(email=email, code=code)

            send_mail(
                subject='ваш код подверждения',
                message = f'Ваш код : {code}',
                from_email = EMAIL_HOST_USER,
                recipient_list = [email]
            )

            return Response({'message' : 'мы отправили код'})
        
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
            )
        

class VerifyCodePassword(APIView):
    def post(self, request):
        serializer = VerifyCodePasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            otp = serializer.validated_data['otp']

            user = User.objects.filter(email=email).first()

            if not user:
                return Response(
                    {'message': 'User with this email does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            user.set_password(new_password)
            user.save()

            otp.delete()

            Token.objects.filter(user=user).delete()

            return Response({
                'message': 'You changed password successfully!'
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
            
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer , ChangePasswordSerialiazer ,ForgotPasswordSerializer,ResetPasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator




class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CustomTokenView(TokenObtainPairView):
#     serializer_class = CustomTokenSerializer
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user=request.user
        data={
            "email":user.email,
            "username":user.username,
            "name":user.name,
            "mobile":user.mobile, 
            "address":user.address,
        }
        return Response(data)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        serializer = ChangePasswordSerialiazer(data=request.data)

        if serializer.is_valid():
            user=request.user
            
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {"error":"Old password is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(
                {"message":"password changed sussesfully"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
User = get_user_model()
class ForgotPasswordView(APIView):
    def post(self,request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)

            reset_link = f"http://127.0.0.1:8000/api/reset-password/{uid}/{token}/"

            send_mail (
                subject="Password Reset",
                message=f"Click link to reset password : {reset_link}",
                from_email="noreply@example.com",
                recipient_list=[email],

            )
            return Response({"message":"password reset link sent"})
        return Response(serializer.errors,status=400)



class ResetPasswordView(APIView):

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id=uid)
        except:
            return Response({"error": "Invalid link"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({"message": "Password reset successful"})

        return Response(serializer.errors, status=400)



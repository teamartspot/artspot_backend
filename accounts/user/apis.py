
from cgitb import lookup
import jwt
import json
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email 
from django.contrib.sites.shortcuts import get_current_site
from .selectors import (
    get_users, 
    get_user_from_email,
)
from .services import create_user
from . services import (
    send_account_activation_email,
    send_reset_password_otp_email,
    save_otp_for_user
)
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from authentication.services import decode_token
from rest_framework.permissions import IsAuthenticated
from .permissions import AllowUnauthorizedUsers
from common.services import codes
from rest_framework_simplejwt.tokens import RefreshToken

# User List API
class UserListApi(APIView):
    permission_classes = (IsAuthenticated, )
    class OutputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        last_name = serializers.CharField()
        first_name = serializers.CharField()


    def get(self, request):
        # Make sure the filters are valid, if passed
        users = get_users()
        user_data = self.OutputSerializer(data=users,  many=True)
        user_data.is_valid(raise_exception=True)

        return Response(user_data.data, status=status.HTTP_200_OK)

# User Create API
class UserCreateApi(generics.CreateAPIView):
    permission_classes = (AllowAny, )

    class RegistrationSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=True)
        last_name = serializers.CharField(required=True)
        email = serializers.EmailField(required=True, validators=[validate_email])
        password = serializers.CharField(required=True)
        password2 = serializers.CharField(required=True)
    
        def validate(self, data):
            if data['password'] != data['password2']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
            return data

    def post(self, request):
        #self.check_object_permissions(self, self.request)
        serializer = self.RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        
        #Create User
        user = create_user(**serializer.validated_data)   

        #Send Activation Email
        current_site = get_current_site(request)
        send_account_activation_email(user, current_site)

        return Response(status=status.HTTP_201_CREATED)

class UserUpdateApi(APIView):
    pass

# User Get API
class UserGetApi(generics.RetrieveAPIView):
    class UserDetailSerializer(serializers.Serializer):
        model = User
        email = serializers.EmailField()
        last_name = serializers.CharField()
        first_name = serializers.CharField()

    serializer_class = UserDetailSerializer
    lookup_field = 'uid'

    def get_queryset(self):
        id = self.kwargs['uid']
        return User.objects.filter(uid=id)


# Verify User API
class UserVerifyApi(APIView): 
    permission_classes = (AllowAny, )

    def get(self, request):
        token = request.GET.get('token')
        data = decode_token(token)
        if data is not None and data['user_id'] is not None:
            user = User.objects.get(email=data['user_id'])
            user.is_verified = True
            user.save()
            return Response('Success', status=status.HTTP_201_CREATED)
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)

# Change Password API
class ChangePasswordApi(generics.UpdateAPIView):
    class ChangePasswordSerializer(serializers.Serializer):
        model = User
        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)
        confirm_new_password = serializers.CharField(required=True)

        def validate(self, data):
            if data['new_password'] != data['confirm_new_password']:
                raise serializers.ValidationError({"password": "New Password fields didn't match."})
            return data

    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=User.objects.all()):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        print(user.email)
        change_password_serializer = self.get_serializer(data=request.data)

        if change_password_serializer.is_valid():
            # Check old password
            if not user.check_password(change_password_serializer.data.get("old_password")):
                return Response({"old_password": ["Old password incorrect"]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(change_password_serializer.data.get("new_password"))
            user.save()
            return Response('success', status=status.HTTP_200_OK)

        return Response(change_password_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Reset Password Request API              
class ResetPasswordRequestApi(APIView):
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        try:
            email = request.POST.get('email')
            user = get_user_from_email(email = email)
       
            if user is not None:
                token = RefreshToken.for_user(user)
                otp = codes.generate_otp()
                save_otp_for_user(user, otp)
                send_reset_password_otp_email(user, otp)
                data = {
                    'refresh': str(token),
                    'access': str(token.access_token)
                }
                    
                return Response(data, status=status.HTTP_200_OK)
            return Response('User does not exist', status=status.HTTP_400_BAD_REQUEST) 

        except:
            return Response('Error while resetting password', status=status.HTTP_400_BAD_REQUEST)

# Reset Password Verify OTP API  
class ResetPasswordVerifyOTPApi(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        try:
            otp = request.POST.get('otp')
            email = request.POST.get('email')
            if otp is not None and email is not None:
               user = get_user_from_email(email=email)
               # Check if OTP matches to the user OTP
               if user is not None:
                    if user.otp == otp:
                        return Response("success", status=status.HTTP_200_OK)
                    else:
                        return Response("Invalid OTP", status=status.HTTP_400_BAD_REQUEST)      
        except:
            return Response('Error while verifying OTP reset password', status=status.HTTP_400_BAD_REQUEST)

# Reset Password API  - Update New Password
class ResetPasswordApi(generics.UpdateAPIView):
    class ResetPasswordSerializer(serializers.Serializer):
        model = User
        email = serializers.EmailField(required=True)
        new_password = serializers.CharField(required=True)
        confirm_new_password = serializers.CharField(required=True)

        def validate(self, data):
            if data['new_password'] != data['confirm_new_password']:
                raise serializers.ValidationError({"password": "New Password fields didn't match."})
            return data

    permission_classes = (IsAuthenticated,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        try:
            reset_password_serializer = self.get_serializer(data=request.data)
            if reset_password_serializer.is_valid():
                email = reset_password_serializer.data.get("email")
                print(email)
                user = get_user_from_email(email=email)
                if user is not None:
                    user.set_password(reset_password_serializer.data.get("new_password"))
                    # After the password is set reset the OTP so that it cannot be used again
                    user.otp = "default"
                    user.save()
                    return Response('success', status=status.HTTP_200_OK)
            return Response(reset_password_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)
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
    send_reset_password_email
)
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from authentication.services import decode_token
from rest_framework.permissions import IsAuthenticated

# User List API
class UserListApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                'first_name',
                'last_name',
                'email'
            )

    def get(self, request):
        # Make sure the filters are valid, if passed
        users = get_users()
        user_data = self.OutputSerializer(data=users)
        user_data.is_valid(raise_exception=True)
        print(user_data)
        return Response(str(user_data))

# User Create API
class UserCreateApi(APIView):
    permission_classes = (AllowAny,)
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

class UserGetApi(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
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
    permission_classes = [AllowAny, ]

    def get(self, request):
        token = request.GET.get('token')
        data = decode_token(token)
        if data is not None and data['user_id'] is not None:
            user = User.objects.get(email=data['user_id'])
            user.is_verified = True
            user.save()
            return Response('Success', status=status.HTTP_201_CREATED)

# API to change user password
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
            
                    
class ResetPasswordApi(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        email = request.POST.get('email')
        current_site = get_current_site(request)
        user = get_user_from_email(email = email)
        if user is not None:
            send_reset_password_email(user, current_site)
            return Response('User does not exist', status=status.HTTP_200_OK)

        return Response('User does not exist', status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmApi():
    pass
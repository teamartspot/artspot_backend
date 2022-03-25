import jwt

from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email 
from django.contrib.sites.shortcuts import get_current_site
from .selectors import get_users
from .services import create_user
from . services import send_account_activation_email
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from authentication.services import decode_token
from rest_framework_simplejwt.tokens import RefreshToken


# User CRUD API
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
        return Response(user_data)

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
        #Create User
        serializer = self.RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        user = create_user(**serializer.validated_data)

        # Send email
        user_email = user.email
        user_first_name = user.first_name
    

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request)
        relative_link = '/users/verify/'
        verification_link = 'http://' + str(current_site) + relative_link + "?token=" + str(token)
       
        send_account_activation_email(verification_link, user_first_name, user_email)

        return Response(status=status.HTTP_201_CREATED)

class UserUpdateApi(APIView):
    pass

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

from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from rest_framework.response import Response
from django.conf import settings
from decouple import config
from .services import jwt_payload_handler_user
from rest_framework import status

# Create your views here.
class LoginApi(TokenObtainPairView):
    class CustomTokenObtainPairSerializer:
        @classmethod
        def get_token(cls, user):
            token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
            # Add custom claims
            token['first_name'] = user.first_name
            return token

    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer
 
class LogoutApi(APIView):
    pass

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print("Before Token : ")
        print(token)
        token['user_email'] = user.email
        print("After Token : ")
        print(token)
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


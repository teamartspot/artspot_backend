from django.urls import path, include
from .apis import (
    UserCreateApi,
    UserUpdateApi,
    UserListApi,
    UserVerifyApi,
    ChangePasswordApi,
    UserGetApi,
    ResetPasswordRequestApi,
    ResetPasswordVerifyOTPApi,
    ResetPasswordApi,
)

user_patterns = [
    path('', UserListApi.as_view(), name='users'),
    path('<str:uid>/', UserGetApi.as_view(), name='user'),
    path('register', UserCreateApi.as_view(), name='register'),
    path('<int:user_id>/update/', UserUpdateApi.as_view(), name='update'),
    path('verify/', UserVerifyApi.as_view(), name ='verify'),
    path('change_password/<str:uid>/', ChangePasswordApi.as_view(), name='change-password'),
    path('reset_password', ResetPasswordRequestApi.as_view(), name='reset-password'),
    path('reset_password/confirm', ResetPasswordVerifyOTPApi.as_view(), name='reset-password'),
    path('reset_password/change', ResetPasswordApi.as_view(), name='reset-password'),
]

user_password_patterns = [
   
]

urlpatterns = [
    path('', include((user_patterns, 'users'))),
]
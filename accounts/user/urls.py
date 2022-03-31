from django.urls import path, include
from .apis import (
    UserCreateApi,
    UserUpdateApi,
    UserListApi,
    UserVerifyApi,
    ChangePasswordApi,
    UserGetApi

)

user_patterns = [
    path('', UserListApi.as_view(), name='users'),
    path('<str:uid>/', UserGetApi.as_view(), name='user'),
    path('register/', UserCreateApi.as_view(), name='register'),
    path('<int:user_id>/update/', UserUpdateApi.as_view(), name='update'),
    path('verify/', UserVerifyApi.as_view(), name ='verify'),
    path('change_password/<str:uid>/', ChangePasswordApi.as_view(), name='change-password')
]

urlpatterns = [
    path('', include((user_patterns, 'users'))),
]
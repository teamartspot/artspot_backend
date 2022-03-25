from django.urls import path, include
from .apis import (
    UserCreateApi,
    UserUpdateApi,
    UserListApi,
    UserVerifyApi,

)

user_patterns = [
    path('', UserListApi.as_view(), name='users'),
    path('register/', UserCreateApi.as_view(), name='register'),
    path('<int:user_id>/update/', UserUpdateApi.as_view(), name='update'),
    path('verify/', UserVerifyApi.as_view(), name = 'verify')
]

urlpatterns = [
    path('', include((user_patterns, 'users'))),
]
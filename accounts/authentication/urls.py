from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .apis import MyTokenObtainPairView
from .views import HelloView


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='get_token'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='refresh_token'),
    path('hello/', HelloView.as_view(), name='hello')
]
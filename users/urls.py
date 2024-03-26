from django.urls import path
from users.apps import UsersConfig
from users.views import UserRegistrationAPIView, UserUpdateAPIView, UserProfileAPIView, UserDeleteAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='user_registration'),
    path('edit/<int:pk>/', UserUpdateAPIView.as_view(), name='update_user'),
    path('<int:pk>/profile/', UserProfileAPIView.as_view(), name='user_profile'),
    path('delete/<int:pk>/', UserDeleteAPIView.as_view(), name='delete_user'),
    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

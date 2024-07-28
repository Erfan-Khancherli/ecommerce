from django.urls import path
from accounts.api import api
from .api.api import RegisterUser , LogoutView , UpdatePassword
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('register1/',RegisterUser.as_view()), #for class base view Register
    path('register/',api.createAccount ),    #for function base view Register
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #login enpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refresh token endpoint
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('change_password/', UpdatePassword.as_view(), name='change_password'),
]
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from jwt_authentication.views import RegisterView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
]

from .views import *
from django.urls import path


urlpatterns = [
    path('', LoginAPIView.as_view(), name='Login_Api'),
    path('SignUp/', SignUp.as_view(), name='Sign_Up_Api'),
    path('UpdateProfile/<int:pk>/', UpdateProfileView.as_view(), name='UpdateProfile_Api'),
]

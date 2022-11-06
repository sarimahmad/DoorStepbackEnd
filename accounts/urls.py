from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', LoginAPIView.as_view(), name='Login_Api'),
    path('SignUp/', SignUp.as_view(), name='Sign_Up_Api'),
    path('UpdateProfile/<int:pk>/', UpdateProfileView.as_view(), name='UpdateProfile_Api'),
    path('ChangePassword/<int:id>/', ChangePassword.as_view(), name='UpdateProfile_Api'),
    path('Chat/<int:id>/', ChatData.as_view(), name='Post_Chat_Api'),
    path('Chat/SenderId/<int:senderId>/ReceiverId/<int:receiverId>/', ChatData.as_view(), name='Get_Chat_Api'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

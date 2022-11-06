from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .Serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import update_last_login


# Create your views here.


class SignUp(APIView):
    serializers_class = SignUpSerializer

    def post(self, request):
        serializers = self.serializers_class(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            user.save()
            data = serializers.data
            refresh = RefreshToken.for_user(user)
            responce_data = {
                'user': data,
                "Token": str(refresh.access_token)
            }

            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializers(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)
        user = SignUpSerializer(user)
        return Response({"Token": str(refresh.access_token), "user": user.data}, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    def post(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        serializers = UpdateProfileSerializer(instance=user, data=request.data)
        if serializers.is_valid():
            serializers.save()
        user = GetUserSerializer(user)
        return Response({"data": user.data})


class ChangePassword(APIView):
    def post(self, request, id):
        password_old = request.data['old_password']
        object = CustomUser.objects.get(id=id)
        if not object.check_password(password_old):
            return Response({"message": "Your Old password not Correct"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        object.set_password(request.data['new_password']);
        object.save()
        return Response({"message": "Your Password has been Changes"}, status=status.HTTP_200_OK)


class ChatData(APIView):
    serializers_class = ChatSerializer

    def post(self, request, id):
        user = CustomUser.objects.get(id=id)
        serializers = self.serializers_class(data=request.data)
        if serializers.is_valid():
            user = serializers.save(user=user)
            user.save()
            data = serializers.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request, senderId, receiverId):
        data = []
        messages = Chat.objects.all()
        for i in messages:
            if i.user.id == senderId or i.user.id == receiverId:
                data.append(i)
        chat_messages = ChatSerializer(data, many=True)
        return Response(chat_messages.data, status=status.HTTP_200_OK)

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
        return Response({"Token": str(refresh.access_token), "User": user.data}, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    def post(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        serializers = UpdateProfileSerializer(instance=user, data=request.data)
        if serializers.is_valid():
            serializers.save()
        return Response({"data": serializers.data})

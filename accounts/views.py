from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .Serializers import *
from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from accounts.Serializers import *
import random


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

    def post(self, request, room_id):
        user = CustomUser.objects.get(id=request.data['user'])
        serializers = self.serializers_class(data=request.data)
        if serializers.is_valid():
            user = serializers.save(user=user , room_id=room_id)
            user.save()
            data = serializers.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request, room_id):
        messages = Chat.objects.filter(room_id=room_id)
        chat_messages = ChatSerializer(messages, many=True)
        return Response(chat_messages.data, status=status.HTTP_200_OK)


class ChatUsers(APIView):

    def post(self, request, user1, user2):
        user_1 = CustomUser.objects.get(id=user1)
        user_2 = CustomUser.objects.get(id=user2)
        room_Already = Check_Room_Data(user_1.room.all(), user_2.room.all())
        print(room_Already)
        if room_Already:
            return Response({"status": 2, "message": 'Room Already Created for these Users'}, status=status.HTTP_200_OK)
        rand_numb = Check_Duplicate_Room()
        room_creation = Room.objects.create(room=rand_numb)
        user_1.room.add(room_creation)
        user_2.room.add(room_creation)
        room_creation.save()
        user_1.save()
        user_2.save()
        return Response({"status": 1, "message": 'Room created for these Users'}, status=status.HTTP_200_OK)

    def get(self, request, user1, user2):
        user = CustomUser.objects.get(id=request.user.id)
        user_all_room = []
        data = user.room.all()
        print(data)
        for j in data:
            users = get_Room_Person(j)
            user_all_room.append({j.id:users})
        return JsonResponse({"data":user_all_room}, status=status.HTTP_200_OK)



def get_Room_Person(room_id):
    room_person = []
    for i in CustomUser.objects.all():
        if room_id in i.room.all():
            serializersed_data = GetUserSerializer(i)
            room_person.append(serializersed_data.data)
    return room_person



def Check_Room_Data(list1, list2):
    if len(list1) > len(list2):
        loop = list2
        checking = list1
    else:
        checking = list2
        loop = list1
    for i in loop:
        if i in checking:
            return True
    return False


def Check_Duplicate_Room():
    rand_numb = random.randint(0, 1000)
    for i in Room.objects.all():
        if rand_numb == i.room:
            Check_Duplicate_Room()
    return rand_numb

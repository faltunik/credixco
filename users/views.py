from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializer import *
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group




# permission
def is_member(user):
    return user.groups.filter(name='Teacher').exists()

# Views for Login



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['id'] = user.id
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



# Views For Creating Users
class CustomUserCreate(APIView):
    permission_classes = (permissions.AllowAny,) # why we are doing this?

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data) # recieving the data, but how? and in which format
        try:
            if serializer.is_valid():  # checking whether data the is valid or not, pm basis of is_valid() function defined in DRF sourcecode            
                user = serializer.save()  # saving the data
                print('User Is: ', user)
                my_group, created = Group.objects.get_or_create(name='Teacher') 
                #my_group.user_set.add(user)
                user.groups.add(my_group)
                print(user)
                if user:
                    json = serializer.data  # no idea what it's doing, need to ask
                    print(json)
                    return Response(json, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error is :"  ,e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for studnets/teacher to get there profile info
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_profile(request):
    print(request.user)
    print(request.user.id)
    #profile = get_object_or_404(Profile, user_id = request.user.id)
    profile = Profile.objects.get(user_id = request.user.id)
    print("__________________Printinh Query__________________")
    print(profile)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)

# for teachers to list their students
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_student(request, format=None):
        if is_member(request.user): 
            print('User is Teacher')
            user = CustomUser.objects.filter(teacher = request.user)
            serializer = CustomUserSerializer(user, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

# for teachers to create their students account
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def create_student(request, format=None):
    if is_member(request.user):
        serializer = CustomUserSerializer(data=request.data)
        print(serializer)
        print(type(serializer))
        if serializer.is_valid():
            serializer.save(teacher = request.user)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)
        







from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'class_name', 'teacher', 'is_teacher')
        extra_kwargs = {'password': {'write_only': True}}  # what is extra_kwargs


    def create(self, validated_data):
        password = validated_data.pop('password', None)  # what it's doing 
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this, but which field
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user')
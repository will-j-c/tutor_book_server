from rest_framework import serializers
from .models import *


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Type
        fields = [
            'type_name'
        ]


class UserSerializer(serializers.ModelSerializer):
    user_type = UserTypeSerializer()
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'user_type',
            'user_uuid',
            'created_at',
            'updated_at',
            'profile_img_url',
        ]


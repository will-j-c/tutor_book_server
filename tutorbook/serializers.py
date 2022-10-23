from rest_framework import serializers
from .models import *

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Type
        fields = [
            'type_name'
        ]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'subject_name'
        ]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = [
            'level_name'
        ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'location_name'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'user_type',
            'user_type',
            'email',
            'user_uuid',
            'created_at',
            'updated_at',
            'profile_img_url',
            'email_is_verified',
        ]

class SkinnyUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                'first_name',
                'profile_img_url',
            ]

class TutorSerializer(serializers.ModelSerializer):
    user = SkinnyUserSerializer(read_only=True)
    locations = LocationSerializer(read_only=True, many=True)
    levels = LevelSerializer(read_only=True, many=True)
    subjects = SubjectSerializer(read_only=True, many=True)

    class Meta:
        model = Tutor
        fields = [
            'user',
            'published',
            'looking_for_assignment',
            'about_me',
            'created_at',
            'updated_at',
            'published_at',
            'subscription_expires_at',
            'locations',
            'levels',
            'subjects',
            'tutor_uuid',
            'average_rating'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'tutor',
            'user',
            'created_at',
            'updated_at',
            'rating',
            'review_text'
        ]

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            'user',
            'published',
            'published_at',
            'created_at',
            'updated_at',
            'filled',
            'title',
            'description',
            'assignment_uuid',
        ]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'tutor',
            'user',
            'sender',
            'created_at',
            'thread',
            'content',
            'is_read',
        ]

class ThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(source='message_set', many=True)
    class Meta:
        model = Thread
        fields = [
            'id',
            'tutor',
            'user',
            'created_at',
            'has_unread',
            'thread_uuid',
            'messages'
        ]
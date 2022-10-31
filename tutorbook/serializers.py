from rest_framework import serializers
from .models import *

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Type
        fields = [
            'id',
            'type_name'
        ]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id',
            'subject_name'
        ]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = [
            'id',
            'level_name'
        ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id',
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
                'id',
                'user_uuid'
            ]

class UUIDUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                'user_uuid',
                'profile_img_url',
                'user_type'
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
            'average_rating',
            'id'
        ]

class SkinnyTutorSerializer(serializers.ModelSerializer):
    user = SkinnyUserSerializer()
    class Meta:
        model = Tutor
        fields = [
            'user',
            'id'
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
    user = SkinnyUserSerializer(read_only=True)
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
    user = SkinnyUserSerializer(read_only=True)
    tutor = SkinnyTutorSerializer(read_only=True)
    class Meta:
        model = Message
        fields = [
            'id',
            'tutor',
            'user',
            'sender',
            'created_at',
            'thread',
            'content',
            'is_read',
        ]

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'tutor',
            'user',
            'sender',
            'thread',
            'content',
        ]

class ThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(source='message_set', many=True)
    user = SkinnyUserSerializer()
    tutor = SkinnyTutorSerializer()
    class Meta:
        model = Thread
        fields = [
            'id',
            'tutor',
            'user',
            'created_at',
            'updated_at',
            'has_unread',
            'thread_uuid',
            'messages'
        ]
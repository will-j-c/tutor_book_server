from email.message import Message
from django.db import models
import uuid

from django.forms import NumberInput
from django.core.validators import DecimalValidator
from static_data import create_choices

# Create your models here.


class User_Type(models.Model):
    type_choices = [('D', 'Default'), ('T', 'Tutor')]
    type_name = models.CharField(max_length=1, choices=type_choices)

    def __str__(self):
        return self.type_name


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    user_type_id = models.ForeignKey(User_Type, on_delete=models.PROTECT)
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_uuid


class Location(models.Model):
    location_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.location_name


class Subject(models.Model):
    subject_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.subject_name


class Level(models.Model):
    level_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.level_name


class Tutor(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    looking_for_assignment = models.BooleanField(default=False)
    about_me = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField()
    subscription_expires_at = models.DateTimeField()
    location = models.ManyToManyField(Location)
    level = models.ManyToManyField(Level)
    subject = models.ManyToManyField(Subject)

    def __str__(self):
        return self.pk


class Assignment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    filled = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class Review(models.Model):
    tutor_id = models.ForeignKey(Tutor, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[DecimalValidator(2, 1)])

    def __str__(self):
        return self.pk

class Thread(models.Model):
    user_one = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_one')
    user_two = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_two')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    thread_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    def __str__(self):
        return self.pk

class Message(models.Model):
    sender_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sender_id')
    receiver_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='receiver_id')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    thread_id = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    def __str__(self):
        return self.pk
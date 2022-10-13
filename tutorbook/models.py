from unittest.util import _MAX_LENGTH
from django.db import models
import uuid

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

class Tutor(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  published = models.BooleanField(default=False)
  looking_for_assignment = models.BooleanField(default=False)
  about_me = models.TextField()
  created_at = models.DateTimeField()
  updated_at = models.DateTimeField()
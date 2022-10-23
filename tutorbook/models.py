from django.db import models
import uuid
from django.core.validators import DecimalValidator

# Create your models here.


class User_Type(models.Model):
    type_name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.type_name


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    email_is_verified = models.BooleanField(default=False)
    user_type = models.ForeignKey(User_Type, on_delete=models.PROTECT)
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    profile_img_url = models.URLField(null=True)

    def __str__(self):
        return str(self.user_uuid)

    def save(self, *args, **kwargs):
        """
        If the type of user is a tutor, also create a bare bones Tutor entry
        """
        if getattr(self, User._meta.get_field('user_type').attname) == 2:
            super().save(*args, **kwargs)
            tutor = Tutor.objects.create(user = self)
            tutor.save()
            return
        super().save(*args, **kwargs) 


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    looking_for_assignment = models.BooleanField(default=False)
    about_me = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    published_at = models.DateTimeField(null=True)
    subscription_expires_at = models.DateTimeField(null=True)
    locations = models.ManyToManyField(Location)
    levels = models.ManyToManyField(Level)
    subjects = models.ManyToManyField(Subject)
    tutor_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.pk)


class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    filled = models.BooleanField(default=False)
    title = models.CharField(max_length=250)
    description = models.TextField()
    assignment_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title


class Review(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[
                                 DecimalValidator(2, 1)])
    review_text = models.TextField(null=True)

    def __str__(self):
        return self.pk


class Thread(models.Model):
    tutor = models.ForeignKey(
        Tutor, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    thread_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    has_unread = models.BooleanField(default=True)

    def __str__(self):
        return self.pk


class Message(models.Model):
    tutor = models.ForeignKey(
        Tutor, on_delete=models.PROTECT, related_name='sender_id')
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='receiver_id')
    tutor_is_sender = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    thread_id = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.pk

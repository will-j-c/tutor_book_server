from .models import User, Tutor
from rest_framework import generics
from .serializers import UserSerializer, TutorSerializer
from .authentication import FirebaseAuthentication

class UserList(generics.CreateAPIView):
    """
    A simple view set to retrieve all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    A simple view to retrieve, update or delete a user
    """
    authentication_classes = [FirebaseAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_uuid'

class TutorList(generics.ListAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

class TutorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    lookup_field = 'tutor_uuid'
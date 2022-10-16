from .models import User
from rest_framework import generics
from .serializers import UserSerializer

class UserList(generics.ListAPIView):
    """
    A simple view set to retrieve all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    A simple view to retrieve, update or delete a user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
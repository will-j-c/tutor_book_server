from .models import Review, User, Tutor
from rest_framework import generics
from .serializers import UserSerializer, TutorSerializer, ReviewSerializer
from .authentication import FirebaseAuthentication
from .permissions import IsOwner

class UserCreate(generics.CreateAPIView):
    """
    A simple view set to retrieve all users
    """
    authentication_classes = []
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    A simple view to retrieve, update or delete a user
    """
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_uuid'

class TutorList(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

class TutorDetail(generics.RetrieveAPIView):
    permission_classes = []
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    lookup_field = 'tutor_uuid'

class ReviewList(generics.ListAPIView):
    permission_classes = []
    serializer_class = ReviewSerializer
    # queryset = Review.objects.all()
    def get_queryset(self):
        tutor_uuid = self.kwargs['tutor_uuid']
        print(tutor_uuid)
        tutor = Tutor.objects.filter(tutor_uuid = tutor_uuid).values()[0]
        print(tutor)
        return Review.objects.filter(tutor = tutor['id'])
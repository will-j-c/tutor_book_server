from .models import Review, User, Tutor, Assignment
from rest_framework import generics
from .serializers import UserSerializer, TutorSerializer, ReviewSerializer, AssignmentSerializer
from .authentication import FirebaseAuthentication
from .permissions import IsOwner

class UserCreate(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_uuid'

class TutorList(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Tutor.objects.filter(published = True)
    serializer_class = TutorSerializer

class TutorDetail(generics.RetrieveAPIView):
    permission_classes = []
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    lookup_field = 'tutor_uuid'

class ReviewList(generics.ListAPIView):
    permission_classes = []
    serializer_class = ReviewSerializer
    def get_queryset(self):
        tutor_uuid = self.kwargs['tutor_uuid']
        tutor = Tutor.objects.filter(tutor_uuid = tutor_uuid).values()[0]
        return Review.objects.filter(tutor = tutor['id'])

class AssignmentList(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Assignment.objects.filter(published = True)
    serializer_class = AssignmentSerializer

class AssignmentCreate(generics.CreateAPIView):
    authentication_classes = []
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentDetail(generics.RetrieveAPIView):
    permission_classes = []
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    lookup_field = 'assignment_uuid'

class AssignmentUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    lookup_field = 'assignment_uuid'
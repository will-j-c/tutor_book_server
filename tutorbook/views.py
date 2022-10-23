from .models import Review, User, Tutor, Assignment, Thread, Message
from rest_framework import generics, views
from .serializers import UserSerializer, TutorSerializer, ReviewSerializer, AssignmentSerializer
from .authentication import FirebaseAuthentication
from .permissions import IsOwner
from rest_framework.response import Response

# User views
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


# Tutor views
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


# Review views
class ReviewList(generics.ListAPIView):
    permission_classes = []
    serializer_class = ReviewSerializer
    def get_queryset(self):
        tutor_uuid = self.kwargs['tutor_uuid']
        tutor = Tutor.objects.filter(tutor_uuid = tutor_uuid).values()[0]
        return Review.objects.filter(tutor = tutor['id'])

class ReviewCreate(generics.CreateAPIView):
    permission_classes = []
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Assignment views
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

class NewThread(views.APIView):
    """
    Creates a new thread and the message in the thread
    """
    permission_classes = []
    def post(self, request):
       data = request.data
       user = User.objects.get(pk = data['user'])
       tutor = Tutor.objects.get(pk = data['tutor'])
       thread = Thread(tutor = tutor, user = user)
       thread.save()
       message = Message(tutor = tutor, user = user, thread_id = thread, content = data.content)
       return Response('hello') 
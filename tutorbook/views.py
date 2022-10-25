from .models import Review, User, Tutor, Assignment, Thread, Message
from rest_framework import generics, views, status
from .serializers import UserSerializer, TutorSerializer, ReviewSerializer, AssignmentSerializer, ThreadSerializer, MessageSerializer, UUIDUserSerializer
from .authentication import FirebaseAuthentication
from .permissions import IsOwner, IsThreadMember
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

class UserDetailEmail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsOwner]
    queryset = User.objects.all()
    serializer_class = UUIDUserSerializer
    lookup_field = 'email'


# Tutor views
class TutorList(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Tutor.objects.filter(published=True)
    serializer_class = TutorSerializer


class TutorDetail(generics.RetrieveAPIView):
    authentication_classes = [FirebaseAuthentication]
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
        tutor = Tutor.objects.filter(tutor_uuid=tutor_uuid).values()[0]
        return Review.objects.filter(tutor=tutor['id'])


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
    queryset = Assignment.objects.filter(published=True)
    serializer_class = AssignmentSerializer


class AssignmentCreate(generics.CreateAPIView):
    permission_classes = []
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

# Messages views


class NewThread(views.APIView):
    """
    Creates a new thread and the message in the thread
    """
    permission_classes = []

    def post(self, request):
        data = request.data
        print(data['user'])
        user = User.objects.get(pk=data['user'])
        tutor = Tutor.objects.get(pk=data['tutor'])
        thread = Thread(tutor=tutor, user=user)
        thread.save()
        message = Message(tutor=tutor, user=user, thread=thread,
                          content=data['content'], sender=data['sender'])
        message.save()
        serialized_thread = ThreadSerializer(thread)
        return Response(status=status.HTTP_201_CREATED, data=serialized_thread.data)


class ThreadDetail(generics.RetrieveAPIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsOwner]
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    lookup_field = 'thread_uuid'


class MessageCreate(generics.CreateAPIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsThreadMember]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageUpdate(generics.UpdateAPIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsOwner]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
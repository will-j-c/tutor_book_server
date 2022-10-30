from .models import Review, User, Tutor, Assignment, Thread, Message
from rest_framework import generics, views, status
from .serializers import CreateMessageSerializer, UserSerializer, TutorSerializer, ReviewSerializer, AssignmentSerializer, ThreadSerializer, MessageSerializer, UUIDUserSerializer
from .authentication import FirebaseAuthentication
from .permissions import IsOwner, IsThreadMember
from rest_framework.response import Response
from django.db.models import Q

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
    pagination_class = None

    def get_queryset(self):
        tutor_uuid = self.kwargs['tutor_uuid']
        tutor = Tutor.objects.filter(tutor_uuid=tutor_uuid).values()[0]
        return Review.objects.filter(tutor=tutor['id'])


class ReviewCreate(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        tutor_uuid = kwargs['tutor_uuid']
        user_uuid = request.data['user']
        tutor = Tutor.objects.get(tutor_uuid=tutor_uuid)
        user = User.objects.get(user_uuid=user_uuid)
        review = Review(user=user, tutor=tutor, rating=request.data['rating'], review_text=request.data['review_text'])
        review.save()
        return Response(status=status.HTTP_201_CREATED)


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


class ThreadUserList(views.APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = []

    def get(self, request):
        print(request.user.pk)
        user = request.user
        tutor = None
        try:
            tutor = Tutor.objects.get(user=user)
        except:
            pass
        if not tutor:
            threads = Thread.objects.filter(user=user)
            serialized_threads = ThreadSerializer(threads, many=True)
            return Response(status=status.HTTP_200_OK, data={'user': 'u', 'threads': serialized_threads.data})
        threads = Thread.objects.filter(tutor=tutor)
        serialized_threads = ThreadSerializer(threads, many=True)
        return Response(status=status.HTTP_200_OK, data={'user': 't', 'threads': serialized_threads.data})


class MessageCreate(generics.CreateAPIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsThreadMember]
    queryset = Message.objects.all()
    serializer_class = CreateMessageSerializer


class MessageUpdate(generics.UpdateAPIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsOwner]
    queryset = Message.objects.all()
    serializer_class = CreateMessageSerializer

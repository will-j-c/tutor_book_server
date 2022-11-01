from datetime import datetime
from .models import Level, Location, Review, Subject, User, Tutor, Assignment, Thread, Message
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


class TutorDetailFromUser(views.APIView):
    permission_classes = []

    def get(self, request):
        print(request.user.pk)
        tutor = Tutor.objects.get(user_id=request.user.pk)
        serialized_tutor = TutorSerializer(tutor)
        return Response(status=status.HTTP_200_OK, data=serialized_tutor.data)

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
        review = Review(user=user, tutor=tutor,
                        rating=request.data['rating'], review_text=request.data['review_text'])
        review.save()
        return Response(status=status.HTTP_201_CREATED)


class ReviewUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Assignment views


class AssignmentList(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Assignment.objects.filter(
        published=True).order_by('-published_at')

    serializer_class = AssignmentSerializer


class AssignmentCreate(views.APIView):
    permission_classes = []

    def post(self, request):
        user = request.user
        assignment = Assignment(user=user, title=request.data['title'], description=request.data[
                                'description'], published=request.data['published'], published_at=datetime.now())
        assignment.save()
        return Response(status=status.HTTP_201_CREATED)


class AssignmentDetail(generics.RetrieveAPIView):
    permission_classes = []
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    lookup_field = 'assignment_uuid'


class AssignmentUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
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
        user = None
        tutor = None
        # Check the source
        data = request.data
        print(data)
        if data['source'] == 'assignment':
            user = User.objects.get(pk=data['user'])
            tutor_user = User.objects.get(user_uuid=data['tutor'])
            tutor = Tutor.objects.get(user_id=tutor_user.pk)

        if data['source'] == 'tutor':
            print(data)
            user = User.objects.get(user_uuid=data['user'])
            tutor = Tutor.objects.get(pk=data['tutor'])
        # Check if a thread already exists between the 2 users
        thread = Thread.objects.filter(Q(user=user), Q(tutor=tutor))
        if thread.exists():
            # Create the message
            message = Message(tutor=tutor, user=user, thread=thread[0],
                              content=data['content'], sender=data['sender'])
            message.save()
            return Response(status=status.HTTP_201_CREATED)

        # Else create the thread and save the message
        thread = Thread(tutor=tutor, user=user)
        thread.save()
        message = Message(tutor=tutor, user=user, thread=thread,
                          content=data['content'], sender=data['sender'])
        message.save()
        
        return Response(status=status.HTTP_201_CREATED)


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
        threads = Thread.objects.filter(tutor=tutor).order_by('updated_at')
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


class StaticData(views.APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = []

    def get(self, request):
        subjects = Subject.objects.all().values()
        locations = Location.objects.all().values()
        levels = Level.objects.all().values()
        print(subjects, locations, levels)
        return Response(status=status.HTTP_200_OK, data={'levels': levels, 'subjects': subjects, 'locations': locations})

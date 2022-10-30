from django.db import router
from django.urls import path
from .views import *

urlpatterns = [
    path('users', UserCreate.as_view(), name='user_list'),
    path('users/<uuid:user_uuid>', UserDetail.as_view(), name='user_detail'),
    path('users/<str:email>', UserDetailEmail.as_view(), name='user_detail_email'),
    path('tutors', TutorList.as_view(), name='tutor_list'),
    path('tutors/<uuid:tutor_uuid>', TutorDetail.as_view(), name='tutor_detail'),
    path('reviews/<uuid:tutor_uuid>',
         ReviewCreate.as_view(), name='review_create'),
    path('reviews/<uuid:tutor_uuid>/list', ReviewList.as_view(), name='review_list'),
    path('reviews/<int:pk>', ReviewUpdateDestroy.as_view(),
         name='review_update_destroy'),
    path('assignments/<uuid:assignment_uuid>',
         AssignmentUpdateDestroy.as_view(), name='assignment_update_destroy'),
    path('assignments/<uuid:assignment_uuid>',
         AssignmentDetail.as_view(), name='assignment_create'),
    path('assignments/create', AssignmentCreate.as_view(),
         name='assignment_create'),
    path('assignments', AssignmentList.as_view(), name='assignment_list'),
    path('threads/<uuid:thread_uuid>',
         ThreadDetail.as_view(), name='thread_detail'),
    path('messages', ThreadUserList.as_view(), name='thread_user_list'),
    path('messages/update/<int:pk>',
         MessageUpdate.as_view(), name='message_update'),
    path('messages/<uuid:thread_uuid>',
         MessageCreate.as_view(), name='message_create'),
    path('messages/new', NewThread.as_view(), name='new_thread'),

]

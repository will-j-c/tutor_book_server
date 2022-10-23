from django.db import router
from django.urls import path
from .views import UserDetail, UserCreate, TutorList, TutorDetail, ReviewList

urlpatterns = [
    path('users/', UserCreate.as_view(), name='user_list'),
    path('users/<uuid:user_uuid>', UserDetail.as_view(), name='user_detail'),
    path('tutors/', TutorList.as_view(), name='tutor_list'),
    path('tutors/<uuid:tutor_uuid>', TutorDetail.as_view(), name='tutor_detail'),
    path('reviews/<uuid:tutor_uuid>', ReviewList.as_view(), name='review_list'),
    # path('assignments', AssignmentList.as_view(), name='assignment_list'),
    # path('assignments', AssignmentList.as_view(), name='assignment_list'),
]
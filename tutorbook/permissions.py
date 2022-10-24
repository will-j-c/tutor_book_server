from rest_framework import permissions
from .models import Tutor, Thread

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        has_permission = False
        print('Checking permission')
        try:
            # Case 1: User wishes to view, update or destroy their own profile
            print('Checking user object vs request user permission')
            has_permission = obj.pk == request.user.pk
            if has_permission:
                print('User level permission')
                return has_permission
        
        except Exception as error:
            print(error)
        
        try:
            # Case 2: Tutor or User is trying to send a message, delete a message or retrieve the message thread for viewing.
            # Need to check if they are a member of the thread. GET methods will be to call the thread. POST and PATCH will be for individual messages
            if request.method == 'GET':
                request_user_id = request.user.pk
                thread_user_id = obj.user_id
                thread_tutor_id = obj.tutor_id
                tutor = Tutor.objects.get(pk = thread_tutor_id)
                has_permission = request_user_id == thread_user_id or request_user_id == tutor.user_id
                if has_permission:
                    return has_permission

        except Exception as error:
            print(error)

        
        return has_permission

class IsThreadMember(permissions.BasePermission):
    """
    Global level permission to only members of a thread to post a message to that thread
    """
    def has_permission(self, request, view):
        has_permission = False
        request_user_id = int(request.user.pk)
        message_thread_id = request.data['thread']
        thread = Thread.objects.get(pk = message_thread_id)
        message_user_id = int(request.data['user'])
        message_tutor_id = int(request.data['tutor'])
        tutor = Tutor.objects.get(pk = thread.tutor_id)
        # Check that the user that sent the request as decoded in JWT is the same user as either the message user or message tutor
        if request_user_id == thread.user_id or request_user_id == tutor.user_id:
            has_permission = True
            return has_permission
        # Check if the thread has matches both user and sender
        if thread.user_id == message_user_id and thread.tutor_id == message_tutor_id:
            has_permission = True
            return has_permission
        
        return has_permission
from rest_framework import permissions
from .models import Tutor, Thread, Message


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
            # Case 2: Call to thread should only allow a GET request and should only allow the user or tutor of the thread to view
            print('Checking that user or tutor is part of this thread')
            if request.method == 'GET':
                request_user_id = request.user.pk
                thread_user_id = obj.user_id
                thread_tutor_id = obj.tutor_id
                tutor = Tutor.objects.get(pk=thread_tutor_id)
                has_permission = request_user_id == thread_user_id or request_user_id == tutor.user_id
                if has_permission:
                    print('Thread level permission granted')
                    return has_permission

        except Exception as error:
            print(error)

        try:
            # Case 3: Check the user is the owner of the comment before updating
            print('Checking that requestor was the sender of the message')
            request_user_id = request.user.pk
            message_object_id = obj.pk
            message = Message.objects.get(pk = message_object_id)
            tutor = Tutor.objects.get(pk = message.tutor_id)
            if message.sender == 'u':
                has_permission = request_user_id == message.user_id
            
            if message.sender == 't':
                has_permission = request_user_id == tutor.user_id

            if has_permission:
                print('Message level permission granted')
                return has_permission

        except Exception as error:
            print(error)

        print('Permission denied')
        return has_permission


class IsThreadMember(permissions.BasePermission):
    """
    Global level permission to only members of a thread to post a message to that thread
    """

    def has_permission(self, request, view):
        has_permission = False
        print('Checking global permission against thread')
        print(request.data)
        print(request.data['tutor'])
        request_user_id = int(request.user.pk)
        print(74)
        message_thread_id = request.data['thread']
        print(76)
        thread = Thread.objects.get(pk=message_thread_id)
        print(78)
        message_user_id = int(request.data['user'])
        print(80)
        message_tutor_id = int(request.data['tutor'])
        print(82)
        tutor = Tutor.objects.get(pk=thread.tutor_id)
        print(tutor)
        # Check that the user that sent the request as decoded in JWT is the same user as either the message user or message tutor
        print(request_user_id == thread.user_id)
        print(request_user_id == tutor.user_id)
        if request_user_id == thread.user_id or request_user_id == tutor.user_id:
            print('hitting line 89')
            has_permission = True
            return has_permission
        # Check if the thread has matches both user and sender
        print(thread.user_id == message_user_id)
        print(thread.tutor_id == message_tutor_id)
        if thread.user_id == message_user_id and thread.tutor_id == message_tutor_id:
            has_permission = True
            return has_permission
        print(has_permission)
        return has_permission

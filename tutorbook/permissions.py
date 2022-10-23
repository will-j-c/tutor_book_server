from rest_framework import permissions
from .models import Tutor

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        has_permission = False
        try:
            tutor = Tutor.objects.get(user_id = request.user.pk)
        except:
            pass
        print('tutor.pk', tutor.pk)
        print('obj.user_id: ', obj.user_id)
        print('request.user.pk: ', request.user.pk)
        print('obj.tutor_id: ', obj.tutor_id)
        # Test if user_id on the object is the as user_id of the request or that the tutor_id matches the tutor id of the user
        try:
            has_permission = obj.user_id == request.user.pk or obj.tutor_id == tutor.pk
        except Exception as error:
            print(error)
            pass
        # If the object is a user itself, test against the pk
        print('object', obj.user_id)
        print('user', request.user.pk)
        return has_permission
from rest_framework import permissions
from .models import User, Assignment

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        has_permission = False
        # Test if user_id on the object is the as user_id of the request
        try:
            has_permission = obj.user_id == request.user.pk
            print(has_permission)
        except Exception as error:
            print(error)
            pass
        # If the object is a user itself, test against the pk
        print('object', obj.user_id)
        print('user', request.user.pk)
        return has_permission
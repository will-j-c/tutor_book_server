from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        print('object', obj)
        print('user', request.user)
        return obj == request.user
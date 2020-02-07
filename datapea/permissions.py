from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the provider of the patient.
        return obj.provider == request.user


class OnlyOwnerReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        print("Request Method: {}".format(request.method))
        if request.method in permissions.SAFE_METHODS:
            return obj.provider == request.user

        # Write permissions are only allowed to the provider of the patient.
        return obj.provider == request.user

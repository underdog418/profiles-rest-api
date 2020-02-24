from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit his/her own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.id == request.user.id

class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self, request,view, obj):
        """check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user_profile.id == request.user.id

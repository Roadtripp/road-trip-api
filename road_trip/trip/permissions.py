from rest_framework import permissions


class TripPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.user:
            return obj.user == request.user
        return False


class CityPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if obj.user:
            return obj.trip.user == request.user
        return False


class ActivityPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if obj.user:
            return obj.trip.user == request.user
        return False

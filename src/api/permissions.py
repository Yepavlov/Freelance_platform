from rest_framework.permissions import BasePermission

from accounts.models import UserType


class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == UserType.Freelancer


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == UserType.Client

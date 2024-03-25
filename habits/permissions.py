from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """ Класс для проверки принадлежности объекта владельцу """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

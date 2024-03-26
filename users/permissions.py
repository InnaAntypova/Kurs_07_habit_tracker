from rest_framework.permissions import BasePermission


class IsUserOwner(BasePermission):
    """ Проверка на владельца объекта """
    def has_object_permission(self, request, view, obj):
        if request.user.pk == obj.pk:
            return True
        return False

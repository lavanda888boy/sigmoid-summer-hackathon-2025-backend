from os import getenv
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class WorkerHeaderPermission(BasePermission):
    def has_permission(self, request, view):
        header_name = getenv('WORKER_PASS_HEADER')
        expected_value = getenv('WORKER_PASS_VALUE')

        if not header_name or not expected_value:
            raise PermissionDenied("Missing worker auth configuration.")

        # Convert env-style header name to Django HTTP header format
        # e.g., 'X-Worker-Secret' -> 'HTTP_X_WORKER_SECRET'
        normalized_header = 'HTTP_' + header_name.upper().replace('-', '_')

        actual_value = request.META.get(normalized_header)
        if actual_value == expected_value:
            return True

        return False

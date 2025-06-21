from rest_framework.permissions import AllowAny
from rest_framework import response, status
from rest_framework.views import APIView


class HealthcheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return response.Response({
            'status': 'ok'
        }, status=status.HTTP_202_ACCEPTED)

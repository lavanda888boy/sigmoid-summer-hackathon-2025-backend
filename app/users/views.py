from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserPreferencesUpdateSerializer


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_preferences(request):
    """
    Overwrites the user's preferred programming languages and domains
    """
    user = request.user
    serializer = UserPreferencesUpdateSerializer(user, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Preferences updated successfully.',
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

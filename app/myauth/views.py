from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import GitHubOAuthCallbackSerializer
from .services import GitHubOAuthService


@api_view(['POST'])
@permission_classes([AllowAny])
def github_oauth_callback(request):
    """
    Handles GitHub OAuth callback

    Expects:
        {
            "code": "github_authorization_code"
        }

    Returns:
        {
            "access": "jwt_access_token",
            "refresh": "jwt_refresh_token",
            "user": {
                "id": 0,
                "username": "github_username",
                "email": "user@example.com",
                "profile_pic_url": "https://avatars.githubusercontent.com/u/github_user_id?v=4",
                "pref_langs": [],
                "pref_domains": []
            }
        }
    """

    serializer = GitHubOAuthCallbackSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        code = serializer.validated_data['code']

        # Exchange code for access token
        access_token = GitHubOAuthService.exchange_code_for_token(code)

        # Get user info from GitHub
        github_user_info = GitHubOAuthService.get_github_user_info(access_token)

        # Create or get user
        user = GitHubOAuthService.create_or_get_user(github_user_info)

        # Generate JWT tokens
        tokens = GitHubOAuthService.generate_jwt_tokens(user)

        # Prepare response data
        response_data = {
            'access': tokens['access'],
            'refresh': tokens['refresh'],
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile_pic_url': user.profile_pic_url,
                'pref_langs': user.pref_langs,
                'pref_domains': user.pref_domains,
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'detail': 'Authentication failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

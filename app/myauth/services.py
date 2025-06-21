import requests
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class GitHubOAuthService:
    @staticmethod
    def exchange_code_for_token(code):
        """Exchange authorization code for access token"""
        url = 'https://github.com/login/oauth/access_token'
        data = {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'code': code,
        }
        headers = {'Accept': 'application/json'}
        
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        
        token_data = response.json()
        if 'error' in token_data:
            raise ValueError(f"GitHub OAuth error: {token_data.get('error_description', 'Unknown error')}")
        
        return token_data.get('access_token')
    
    @staticmethod
    def get_github_user_info(access_token):
        """Get user information from GitHub API"""
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Get user info
        user_response = requests.get('https://api.github.com/user', headers=headers)
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Get user emails (primary email might be private)
        email_response = requests.get('https://api.github.com/user/emails', headers=headers)
        email_response.raise_for_status()
        emails_data = email_response.json()
        
        # Find primary email
        primary_email = None
        for email_info in emails_data:
            if email_info.get('primary', False):
                primary_email = email_info['email']
                break
        
        return {
            'username': user_data.get('login'),
            'email': primary_email or user_data.get('email'),
            'github_id': user_data.get('id'),
            'avatar_url': user_data.get('avatar_url'),
        }
    
    @staticmethod
    def create_or_get_user(github_user_info):
        """Create or get user based on GitHub info"""
        username = github_user_info['username']
        email = github_user_info['email']
        profile_pic_url = github_user_info['avatar_url']
        
        if not email:
            raise ValueError("No email provided by GitHub")
        
        # Try to find existing user by email or username
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                # Update email if user exists but with different email
                if user.email != email:
                    user.email = email
                    user.save()
            except User.DoesNotExist:
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    profile_pic_url=profile_pic_url,
                )
        
        return user
    
    @staticmethod
    def generate_jwt_tokens(user):
        """Generate JWT tokens for user"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

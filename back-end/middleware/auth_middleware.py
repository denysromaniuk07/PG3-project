"""
Custom authentication middleware for JWT and session-based auth.
Handles token validation and user context enrichment.
"""

import logging
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from api.models import User

logger = logging.getLogger(__name__)


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to handle JWT authentication from Authorization header.
    Validates JWT tokens and sets authenticated user on request.
    
    Usage: Add 'middleware.auth_middleware.JWTAuthenticationMiddleware' to MIDDLEWARE
    """

    def process_request(self, request):
        """Extract and validate JWT token from Authorization header."""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        
        if len(auth_header) == 2 and auth_header[0].lower() == 'bearer':
            token = auth_header[1]
            try:
                # Validate token
                validated_token = self._validate_token(token)
                user_id = validated_token.get('user_id')
                
                if user_id:
                    try:
                        user = User.objects.get(id=user_id)
                        request.user = user
                        request.auth = token
                        logger.debug(f"JWT authenticated user: {user.username}")
                    except User.DoesNotExist:
                        logger.warning(f"JWT token references non-existent user ID: {user_id}")
                        request.user = AnonymousUser()
            except (InvalidToken, TokenError) as e:
                logger.warning(f"Invalid JWT token: {str(e)}")
                request.user = AnonymousUser()
        
        return None

    @staticmethod
    def _validate_token(token):
        """Validate JWT token and return decoded data."""
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            decoded_token = AccessToken(token)
            return dict(decoded_token)
        except Exception as e:
            raise InvalidToken(str(e))


class UserContextMiddleware(MiddlewareMixin):
    """
    Enriches request with user context data.
    Adds user profile info, permissions, and cached data to request.
    
    Usage: Add 'middleware.auth_middleware.UserContextMiddleware' to MIDDLEWARE
    """

    def process_request(self, request):
        """Add user context to request object."""
        request.user_context = {
            'is_authenticated': request.user.is_authenticated,
            'user_id': request.user.id if request.user.is_authenticated else None,
            'username': request.user.username if request.user.is_authenticated else None,
            'is_staff': request.user.is_staff if request.user.is_authenticated else False,
            'is_superuser': request.user.is_superuser if request.user.is_authenticated else False,
        }
        
        if request.user.is_authenticated:
            try:
                request.user_context.update({
                    'points': request.user.points,
                    'is_mentor': request.user.is_mentor,
                    'is_premium': request.user.is_premium,
                    'location': request.user.location,
                    'title': request.user.title,
                })
            except Exception as e:
                logger.warning(f"Error enriching user context: {str(e)}")
        
        return None


class TokenBlacklistMiddleware(MiddlewareMixin):
    """
    Checks if JWT token is blacklisted (e.g., user logged out).
    Prevents use of revoked tokens.
    
    Note: Requires TokenBlacklist model implementation
    Usage: Add 'middleware.auth_middleware.TokenBlacklistMiddleware' to MIDDLEWARE
    """

    def process_request(self, request):
        """Check if token is blacklisted."""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        
        if len(auth_header) == 2 and auth_header[0].lower() == 'bearer':
            token = auth_header[1]
            
            # Check if token is blacklisted
            # This would require a TokenBlacklist model
            # For now, this is a placeholder for future implementation
            try:
                from api.models import TokenBlacklist
                if TokenBlacklist.objects.filter(token=token).exists():
                    logger.warning("Attempt to use blacklisted token")
                    request.user = AnonymousUser()
            except (ImportError, Exception):
                pass
        
        return None

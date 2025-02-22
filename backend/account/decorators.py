from functools import wraps
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from account.models import User

def verify_token_return_user(view_func):
    """
    Decorator to extract JWT token from request, validate it,
    and pass the authenticated user to the view function.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Extract the token from the 'Authorization' header or cookies
        token = None

        if 'x-access-token' in request.COOKIES:
            token = request.COOKIES['x-access-token']

        if not token:
            return JsonResponse({'error': 'Access token is missing or invalid'}, status=401)

        try:
            unt_token = UntypedToken(token)
            user_id = unt_token.payload.get('user_id')

            user = User.objects.get(id=user_id)
        except (InvalidToken, TokenError):
            return JsonResponse({'error': 'Invalid or expired token'}, status=498)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Pass the user as an argument to the view function
        return view_func(request, *args, user=user, **kwargs)

    return _wrapped_view

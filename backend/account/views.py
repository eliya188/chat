from django.contrib.auth import authenticate
from django.contrib.auth.models import UserManager
from django.http import JsonResponse
from .models import User
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
@require_http_methods(["POST"])
def create_user_view(request):
    try:
        data = json.loads(request.body)
        password = data.get('password')
        email = data.get('email')

        if not email:
            return JsonResponse({'error': 'Email field is required'}, status=400)

        user_manager = UserManager()
        email = user_manager.normalize_email(email)
        user = User(email=email, username=data.get("username"), password=password)
        user.set_password(password)
        user.save()

        user = authenticate(email=email, password=password)
        return JsonResponse({'status': 'success'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# @csrf_exempt
# @require_http_methods(["POST"])
# def create_superuser(request):
#     extra_fields.setdefault('is_superuser', True)
#     return self.create_user(username, password, email, **extra_fields)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try: 
        data = json.loads(request.body)

        user = authenticate(email=data.get("email"), password=data.get("password"))
        if user:
            refresh = RefreshToken.for_user(user=user)
            access_token = str(refresh.access_token)

            response = JsonResponse({'status': 'success'}, status=200)
            response.set_cookie( 'access_token', access_token, httponly=True, samesite='Lax', secure=True if request.is_secure() else False )
            return response
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
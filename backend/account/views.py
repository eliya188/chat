from django.contrib.auth import authenticate
from django.contrib.auth.models import UserManager
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from account.decorators  import verify_token_return_user
from account.utils import *
from .models import User
import json

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

        refresh, access_token = generate_tokens(user=user)
        response = JsonResponse({'status': 'success'}, status=201)
        response.set_cookie( 'x-access-token', access_token, httponly=True, samesite='Lax', secure=True if request.is_secure() else False )
        response.set_cookie( 'x-refresh', str(refresh), httponly=True,  samesite='Lax', secure=True if request.is_secure() else False)   
        return response
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

        user = authenticate(email=data.get('email'), password=data.get('password'))
        if user:
            refresh, access_token = generate_tokens(user=user)

            response = JsonResponse({'status': 'success'}, status=200)
            response.set_cookie( 'x-access-token', access_token, httponly=True, samesite='Lax', secure=True if request.is_secure() else False )
            response.set_cookie( 'x-refresh', str(refresh), httponly=True,  samesite='Lax', secure=True if request.is_secure() else False)            
            return response
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@verify_token_return_user
@csrf_exempt
@require_http_methods(["GET"])
def logout(request, user):
    response = JsonResponse({'status': 'success'}, status=200)
    response.delete_cookie('x-access-token')
    response.delete_cookie('x-refresh')
    return response

@csrf_exempt
@require_http_methods(["POST"])
def refresh_access_token(request):
    data = json.loads(request.body)
    refresh_token = data.get('x-refresh')
    if not refresh_token:
        return HttpResponse({'error': 'Refresh token is required'}, status=400)
    
    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = refresh.access_token
        response = JsonResponse({'status': 'success'}, status=200)
        response.set_cookie( 'x-access-token', new_access_token, httponly=True, samesite='Lax', secure=True if request.is_secure() else False )
        return response
    except Exception as e:
        return HttpResponse({'error': str(e)}, status=400)
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', create_user_view, name='create_user'),
    # path('delete/', delete_user, name='delete_user')
    path('logout/', logout, name='logout'),
    path('refresh/', refresh_access_token, name='refresh_access_token')
]
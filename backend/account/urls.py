from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', create_user_view, name='create_user')
    # path('logout/', views.logout_view, name='logout'),
    # Add other URL patterns for your account app here
]
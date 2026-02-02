from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.get_user_profile, name='user_profile'),
    path('preferences/', views.user_preferences, name='user_preferences'),
]

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, LoginSerializer, UserPreferencesSerializer
from .models import UserPreferences


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    User registration endpoint.
    
    POST /api/auth/register/
    {
        "username": "newuser",
        "email": "user@example.com",
        "password": "securepass",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    
    # Validation
    if not username or not password:
        return Response(
            {'error': 'Username and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(password) < 6:
        return Response(
            {'error': 'Password must be at least 6 characters long.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if email already exists
    if email and User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already registered.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create default preferences for new user
        UserPreferences.objects.create(user=user)
        
        # Auto-login after registration
        login(request, user)
        
        user_data = UserSerializer(user).data
        return Response({
            'message': 'Registration successful.',
            'user': user_data
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {'error': f'Registration failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint using Basic Authentication.
    
    POST /api/auth/login/
    {
        "username": "user",
        "password": "pass"
    }
    """
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid credentials format.', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        user_data = UserSerializer(user).data
        return Response({
            'message': 'Login successful.',
            'user': user_data
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Invalid username or password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint.
    
    POST /api/auth/logout/
    """
    logout(request)
    return Response(
        {'message': 'Logout successful.'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Get current user profile with statistics.
    
    GET /api/auth/profile/
    """
    user = request.user
    
    # Ensure user has preferences
    if not hasattr(user, 'preferences'):
        UserPreferences.objects.create(user=user)
    
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_preferences(request):
    """
    Get or update user preferences.
    
    GET /api/auth/preferences/
    PUT/PATCH /api/auth/preferences/
    {
        "theme": "dark",
        "default_view": "charts",
        "items_per_page": 25,
        "default_sort_column": "equipment_name",
        "default_sort_order": "asc",
        "last_active_dataset_id": 5
    }
    """
    # Get or create preferences
    preferences, created = UserPreferences.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        serializer = UserPreferencesSerializer(preferences)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update preferences
    serializer = UserPreferencesSerializer(preferences, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


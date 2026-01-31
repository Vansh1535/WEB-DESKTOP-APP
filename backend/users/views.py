from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, LoginSerializer


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

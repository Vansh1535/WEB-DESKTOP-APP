from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPreferences


class UserPreferencesSerializer(serializers.ModelSerializer):
    """Serializer for UserPreferences model."""
    class Meta:
        model = UserPreferences
        fields = [
            'theme', 'default_view', 'items_per_page',
            'default_sort_column', 'default_sort_order',
            'last_active_dataset_id', 'updated_at'
        ]
        read_only_fields = ['updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    preferences = UserPreferencesSerializer(read_only=True, allow_null=True)
    upload_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'preferences', 'upload_count']
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_upload_count(self, obj):
        return obj.datasets.count()
    
    def to_representation(self, instance):
        """Ensure preferences exist before serialization."""
        # Create preferences if they don't exist
        if not hasattr(instance, 'preferences'):
            UserPreferences.objects.get_or_create(user=instance)
            instance.refresh_from_db()
        return super().to_representation(instance)


class LoginSerializer(serializers.Serializer):
    """
    Serializer for login credentials.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

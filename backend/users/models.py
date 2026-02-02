from django.db import models
from django.contrib.auth.models import User


class UserPreferences(models.Model):
    """Store user preferences and settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    # Theme and display preferences
    theme = models.CharField(
        max_length=10, 
        default='light',
        choices=[('light', 'Light'), ('dark', 'Dark')]
    )
    default_view = models.CharField(
        max_length=20, 
        default='charts',
        choices=[('charts', 'Charts'), ('data', 'Data Table'), ('history', 'History')]
    )
    
    # Table preferences
    items_per_page = models.IntegerField(default=10)
    default_sort_column = models.CharField(max_length=50, blank=True, default='')
    default_sort_order = models.CharField(
        max_length=4,
        default='asc',
        choices=[('asc', 'Ascending'), ('desc', 'Descending')]
    )
    
    # Session data
    last_active_dataset_id = models.IntegerField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'User preferences'
    
    def __str__(self):
        return f"{self.user.username}'s preferences"

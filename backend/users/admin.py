from django.contrib import admin
from .models import UserPreferences


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'default_view', 'items_per_page', 'last_active_dataset_id', 'updated_at')
    list_filter = ('theme', 'default_view')
    search_fields = ('user__username', 'user__email')

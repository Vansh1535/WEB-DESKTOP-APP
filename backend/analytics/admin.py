from django.contrib import admin
from .models import CSVDataset


@admin.register(CSVDataset)
class CSVDatasetAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'uploaded_by', 'uploaded_at', 'status', 'row_count']
    list_filter = ['status', 'uploaded_at', 'uploaded_by']
    search_fields = ['file_name', 'uploaded_by__username']
    readonly_fields = ['uploaded_at', 'processed_at', 'row_count', 'statistics', 'error_log']
    
    fieldsets = (
        ('File Information', {
            'fields': ('file_name', 'file', 'uploaded_by')
        }),
        ('Processing Status', {
            'fields': ('status', 'row_count', 'uploaded_at', 'processed_at')
        }),
        ('Statistics', {
            'fields': ('statistics',),
            'classes': ('collapse',)
        }),
        ('Errors', {
            'fields': ('error_log',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Prevent manual addition through admin
        return False

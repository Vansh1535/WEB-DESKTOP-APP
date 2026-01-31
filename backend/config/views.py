from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    """
    Welcome page with API information.
    """
    return JsonResponse({
        'message': 'Welcome to Chemical Equipment Parameter Visualizer API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'authentication': {
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/'
            },
            'analytics': {
                'upload_csv': '/api/analytics/csv/upload/',
                'list_datasets': '/api/analytics/csv/datasets/',
                'get_dataset': '/api/analytics/csv/datasets/{id}/',
                'delete_dataset': '/api/analytics/csv/datasets/{id}/',
                'statistics': '/api/analytics/statistics/'
            }
        },
        'documentation': 'See README.md for full documentation',
        'authentication': 'All endpoints (except login) require HTTP Basic Authentication'
    })

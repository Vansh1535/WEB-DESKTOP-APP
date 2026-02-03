from django.urls import path
from . import views

urlpatterns = [
    path('csv/upload/', views.upload_csv, name='upload-csv'),
    path('datasets/', views.list_datasets, name='list-datasets'),
    path('datasets/<int:pk>/', views.retrieve_dataset, name='retrieve-dataset'),
    path('datasets/<int:pk>/statistics/', views.get_dataset_statistics, name='dataset-statistics'),
    path('datasets/<int:pk>/data/', views.get_dataset_data, name='dataset-data'),
    path('datasets/<int:pk>/pdf-report/', views.generate_pdf_report, name='generate-pdf'),
    path('csv/statistics/', views.get_statistics, name='get-statistics'),
]

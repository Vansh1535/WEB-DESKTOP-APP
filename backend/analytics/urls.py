from django.urls import path
from . import views

urlpatterns = [
    path('csv/upload/', views.upload_csv, name='upload-csv'),
    path('csv/datasets/', views.list_datasets, name='list-datasets'),
    path('csv/datasets/<int:pk>/', views.retrieve_dataset, name='retrieve-dataset'),
    path('csv/datasets/<int:pk>/', views.delete_dataset, name='delete-dataset'),
    path('csv/datasets/<int:pk>/pdf/', views.generate_pdf_report, name='generate-pdf'),
    path('csv/statistics/', views.get_statistics, name='get-statistics'),
]

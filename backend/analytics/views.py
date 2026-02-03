from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import CSVDataset
from .serializers import (
    CSVDatasetSerializer,
    CSVUploadSerializer,
    StatisticsSerializer
)
from .services import CSVProcessingService
from .pdf_service import PDFReportService


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_csv(request):
    """
    Upload and process a CSV file.
    
    POST /api/analytics/csv/upload/
    Content-Type: multipart/form-data
    
    Form data:
        file: CSV file
    
    Returns:
        {
            "dataset_id": 1,
            "file_name": "equipment.csv",
            "status": "completed",
            "statistics": {...}
        }
    """
    serializer = CSVUploadSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid file upload.', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    uploaded_file = serializer.validated_data['file']
    
    # Create dataset instance
    dataset = CSVDataset.objects.create(
        file_name=uploaded_file.name,
        file=uploaded_file,
        uploaded_by=request.user,
        status='processing'
    )
    
    # Process CSV
    processor = CSVProcessingService(dataset)
    success, error_message = processor.process()
    
    if not success:
        return Response(
            {
                'error': 'CSV processing failed.',
                'details': error_message,
                'dataset_id': dataset.id
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Return success response
    dataset.refresh_from_db()
    return Response(
        {
            'message': 'CSV uploaded and processed successfully.',
            'dataset_id': dataset.id,
            'file_name': dataset.file_name,
            'status': dataset.status,
            'row_count': dataset.row_count,
            'statistics': dataset.statistics
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_datasets(request):
    """
    List all datasets for the authenticated user.
    
    GET /api/analytics/csv/datasets/
    
    Returns:
        {
            "count": 5,
            "datasets": [...]
        }
    """
    datasets = CSVDataset.objects.filter(uploaded_by=request.user)
    serializer = CSVDatasetSerializer(datasets, many=True)
    
    return Response(
        {
            'count': datasets.count(),
            'datasets': serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_dataset(request, pk):
    """
    Retrieve a specific dataset by ID.
    
    GET /api/analytics/datasets/{id}/
    
    Returns:
        {
            "id": 1,
            "file_name": "equipment.csv",
            "status": "completed",
            "statistics": {...},
            ...
        }
    """
    dataset = get_object_or_404(CSVDataset, pk=pk, uploaded_by=request.user)
    serializer = CSVDatasetSerializer(dataset)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_statistics(request, pk):
    """
    Get statistics for a specific dataset.
    
    GET /api/analytics/datasets/{id}/statistics/
    
    Returns:
        Statistics dictionary from the dataset
    """
    dataset = get_object_or_404(CSVDataset, pk=pk, uploaded_by=request.user)
    
    if dataset.status != 'completed':
        return Response(
            {'error': 'Dataset processing not completed.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not dataset.statistics:
        return Response(
            {'error': 'No statistics available for this dataset.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    return Response(dataset.statistics, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dataset(request, pk):
    """
    Delete a specific dataset by ID.
    
    DELETE /api/analytics/csv/datasets/{id}/
    
    Returns:
        {
            "message": "Dataset deleted successfully."
        }
    """
    dataset = get_object_or_404(CSVDataset, pk=pk, uploaded_by=request.user)
    
    # Delete the file from storage
    if dataset.file:
        dataset.file.delete(save=False)
    
    # Delete the database record
    dataset.delete()
    
    return Response(
        {'message': 'Dataset deleted successfully.'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_statistics(request):
    """
    Get aggregated statistics from the most recent completed dataset.
    
    GET /api/v1/analytics/csv/statistics/
    
    Returns:
        {
            "total_equipment_count": 150,
            "by_type": {
                "Pump": {"count": 50, "flowrate": {...}, ...},
                ...
            },
            "overall_averages": {
                "flowrate": 245.6,
                "pressure": 8.2,
                "temperature": 112.4
            }
        }
    """
    # Get the most recent completed dataset
    latest_dataset = CSVDataset.objects.filter(
        uploaded_by=request.user,
        status='completed'
    ).order_by('-uploaded_at').first()
    
    if not latest_dataset or not latest_dataset.statistics:
        return Response(
            {
                'error': 'No statistics available. Please upload a CSV file.'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Return the statistics from the latest dataset
    return Response(
        latest_dataset.statistics,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_data(request, pk):
    """
    Get raw CSV data from a specific dataset.
    
    GET /api/analytics/datasets/{id}/data/
    
    Returns:
        List of equipment data rows
    """
    dataset = get_object_or_404(CSVDataset, pk=pk, uploaded_by=request.user)
    
    if dataset.status != 'completed':
        return Response(
            {'error': 'Dataset processing not completed.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        import pandas as pd
        df = pd.read_csv(dataset.file.path)
        data = df.to_dict('records')
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Failed to read dataset: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request, pk):
    """
    Generate and download PDF report for a specific dataset.
    
    GET /api/analytics/datasets/{id}/pdf-report/
    
    Returns:
        PDF file download
    """
    dataset = get_object_or_404(CSVDataset, pk=pk, uploaded_by=request.user)
    
    if dataset.status != 'completed':
        return Response(
            {'error': 'Cannot generate PDF for incomplete dataset.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Generate PDF
    pdf_service = PDFReportService(dataset)
    pdf_bytes = pdf_service.generate()
    
    # Create HTTP response with PDF
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}.pdf"'
    
    return response

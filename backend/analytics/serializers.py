from rest_framework import serializers
from .models import CSVDataset


class CSVDatasetSerializer(serializers.ModelSerializer):
    """
    Serializer for CSVDataset model.
    """
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = CSVDataset
        fields = [
            'id',
            'file_name',
            'file',
            'uploaded_by',
            'uploaded_by_username',
            'uploaded_at',
            'row_count',
            'status',
            'statistics',
            'error_log',
            'processed_at'
        ]
        read_only_fields = [
            'id',
            'uploaded_by',
            'uploaded_by_username',
            'uploaded_at',
            'row_count',
            'status',
            'statistics',
            'error_log',
            'processed_at'
        ]


class CSVUploadSerializer(serializers.Serializer):
    """
    Serializer for CSV file upload.
    """
    file = serializers.FileField(required=True)

    def validate_file(self, value):
        """
        Validate that the uploaded file is a CSV.
        """
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 10MB.")
        
        return value


class StatisticsSerializer(serializers.Serializer):
    """
    Serializer for combined statistics response.
    """
    total_datasets = serializers.IntegerField()
    total_equipment_count = serializers.IntegerField()
    datasets = CSVDatasetSerializer(many=True)

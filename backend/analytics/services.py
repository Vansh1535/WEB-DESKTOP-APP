import pandas as pd
import logging
from django.conf import settings
from django.utils import timezone
from .models import CSVDataset

logger = logging.getLogger(__name__)


class CSVProcessingService:
    """
    Service class to handle CSV file processing and statistics computation.
    """
    
    REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    NUMERIC_COLUMNS = ['Flowrate', 'Pressure', 'Temperature']
    
    def __init__(self, dataset_instance):
        """
        Initialize the service with a CSVDataset instance.
        
        Args:
            dataset_instance: CSVDataset model instance
        """
        self.dataset = dataset_instance
    
    def validate_csv(self, df):
        """
        Validate CSV structure and data.
        
        Args:
            df: pandas DataFrame
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Check if DataFrame is empty
        if df.empty:
            return False, "CSV file is empty."
        
        # Check required columns
        missing_columns = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Check for non-negative numeric values
        for col in self.NUMERIC_COLUMNS:
            if col in df.columns:
                # Convert to numeric, coerce errors to NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Check for NaN values
                if df[col].isna().any():
                    return False, f"Column '{col}' contains non-numeric values."
                
                # Check for negative values
                if (df[col] < 0).any():
                    return False, f"Column '{col}' contains negative values."
        
        return True, None
    
    def compute_statistics(self, df):
        """
        Compute statistics from the DataFrame.
        
        Args:
            df: pandas DataFrame
            
        Returns:
            dict: Computed statistics
        """
        # Total equipment count
        total_count = len(df)
        
        # Group by Type
        grouped = df.groupby('Type')
        
        # Statistics by type
        type_statistics = {}
        for equipment_type, group in grouped:
            type_statistics[equipment_type] = {
                'count': len(group),
                'flowrate': {
                    'avg': round(float(group['Flowrate'].mean()), 2),
                    'min': round(float(group['Flowrate'].min()), 2),
                    'max': round(float(group['Flowrate'].max()), 2),
                },
                'pressure': {
                    'avg': round(float(group['Pressure'].mean()), 2),
                    'min': round(float(group['Pressure'].min()), 2),
                    'max': round(float(group['Pressure'].max()), 2),
                },
                'temperature': {
                    'avg': round(float(group['Temperature'].mean()), 2),
                    'min': round(float(group['Temperature'].min()), 2),
                    'max': round(float(group['Temperature'].max()), 2),
                }
            }
        
        # Overall averages
        overall_averages = {
            'flowrate': round(float(df['Flowrate'].mean()), 2),
            'pressure': round(float(df['Pressure'].mean()), 2),
            'temperature': round(float(df['Temperature'].mean()), 2),
        }
        
        return {
            'total_equipment_count': total_count,
            'by_type': type_statistics,
            'overall_averages': overall_averages
        }
    
    def process(self):
        """
        Process the CSV file: validate, compute statistics, and update the dataset.
        
        Returns:
            tuple: (success, error_message)
        """
        try:
            # Update status to processing
            self.dataset.status = 'processing'
            self.dataset.save()
            
            # Read CSV file
            df = pd.read_csv(self.dataset.file.path)
            
            # Validate CSV
            is_valid, error_message = self.validate_csv(df)
            if not is_valid:
                self.dataset.status = 'failed'
                self.dataset.error_log = error_message
                self.dataset.processed_at = timezone.now()
                self.dataset.save()
                return False, error_message
            
            # Compute statistics
            statistics = self.compute_statistics(df)
            
            # Update dataset
            self.dataset.row_count = len(df)
            self.dataset.statistics = statistics
            self.dataset.status = 'completed'
            self.dataset.processed_at = timezone.now()
            self.dataset.save()
            
            logger.info(f"Successfully processed dataset {self.dataset.id}")
            return True, None
            
        except Exception as e:
            error_message = f"Error processing CSV: {str(e)}"
            logger.error(error_message)
            
            self.dataset.status = 'failed'
            self.dataset.error_log = error_message
            self.dataset.processed_at = timezone.now()
            self.dataset.save()
            
            return False, error_message

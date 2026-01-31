from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class CSVDataset(models.Model):
    """
    Model to store uploaded CSV datasets with computed statistics.
    """
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='csv_uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    row_count = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    statistics = models.JSONField(null=True, blank=True)
    error_log = models.TextField(null=True, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'CSV Dataset'
        verbose_name_plural = 'CSV Datasets'

    def __str__(self):
        return f"{self.file_name} - {self.uploaded_by.username}"


@receiver(post_save, sender=CSVDataset)
def manage_user_dataset_limit(sender, instance, created, **kwargs):
    """
    Automatically delete old datasets when user exceeds the limit.
    Keep only the last MAX_DATASETS_PER_USER datasets per user.
    """
    if created:
        user = instance.uploaded_by
        max_datasets = getattr(settings, 'MAX_DATASETS_PER_USER', 5)
        
        # Get all datasets for this user, ordered by upload date (newest first)
        user_datasets = CSVDataset.objects.filter(uploaded_by=user).order_by('-uploaded_at')
        
        # If user has more than allowed, delete the oldest ones
        if user_datasets.count() > max_datasets:
            datasets_to_delete = user_datasets[max_datasets:]
            for dataset in datasets_to_delete:
                dataset.file.delete(save=False)  # Delete the file from storage
                dataset.delete()  # Delete the database record

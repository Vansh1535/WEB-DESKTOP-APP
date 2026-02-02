"""
Comprehensive integration test for the entire application flow.
Tests: Authentication, CSV Upload, Statistics, PDF Generation
"""

import os
import base64
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from analytics.models import CSVDataset


class CompleteFlowTestCase(TestCase):
    """Test complete application workflow"""
    
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create Basic Auth header
        credentials = base64.b64encode(b'testuser:testpass123').decode('ascii')
        self.auth_header = f'Basic {credentials}'
    
    def test_01_authentication(self):
        """Test user authentication"""
        response = self.client.post(
            '/api/v1/auth/login/',
            data={'username': 'testuser', 'password': 'testpass123'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('user', data)
        self.assertEqual(data['user']['username'], 'testuser')
        print("✓ Authentication test passed")
    
    def test_02_invalid_authentication(self):
        """Test invalid credentials"""
        response = self.client.post(
            '/api/v1/auth/login/',
            data={'username': 'testuser', 'password': 'wrongpass'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        print("✓ Invalid authentication test passed")
    
    def test_03_csv_upload(self):
        """Test CSV file upload"""
        # Create sample CSV content
        csv_content = b"""equipment name,type,flowrate,pressure,temperature
Reactor A,Reactor,150.5,10.2,85.3
Pump B,Pump,200.0,15.5,45.2
Heat Exchanger C,Heat Exchanger,180.3,12.1,95.7"""
        
        csv_file = SimpleUploadedFile(
            "test_equipment.csv",
            csv_content,
            content_type="text/csv"
        )
        
        response = self.client.post(
            '/api/v1/analytics/csv/upload/',
            {'file': csv_file},
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('dataset_id', data)
        self.assertIn('statistics', data)
        self.assertEqual(data['row_count'], 3)
        
        # Store dataset_id for other tests
        self.dataset_id = data['dataset_id']
        print("✓ CSV upload test passed")
        return data['dataset_id']
    
    def test_04_list_datasets(self):
        """Test listing datasets"""
        # First upload a dataset
        self.test_03_csv_upload()
        
        response = self.client.get(
            '/api/v1/analytics/csv/datasets/',
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('datasets', data)
        self.assertGreater(len(data['datasets']), 0)
        print("✓ List datasets test passed")
    
    def test_05_get_statistics(self):
        """Test getting statistics"""
        # First upload a dataset
        self.test_03_csv_upload()
        
        response = self.client.get(
            '/api/v1/analytics/csv/statistics/',
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total_equipment_count', data)
        self.assertIn('overall_averages', data)
        self.assertIn('by_type', data)
        print("✓ Statistics test passed")
    
    def test_06_pdf_generation(self):
        """Test PDF report generation"""
        # First upload a dataset
        dataset_id = self.test_03_csv_upload()
        
        response = self.client.get(
            f'/api/v1/analytics/csv/datasets/{dataset_id}/pdf/',
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertGreater(len(response.content), 0)
        print("✓ PDF generation test passed")
    
    def test_07_delete_dataset(self):
        """Test deleting a dataset"""
        # First upload a dataset
        dataset_id = self.test_03_csv_upload()
        
        response = self.client.delete(
            f'/api/v1/analytics/csv/datasets/{dataset_id}/',
            HTTP_AUTHORIZATION=self.auth_header
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify it's deleted
        self.assertFalse(
            CSVDataset.objects.filter(id=dataset_id).exists()
        )
        print("✓ Delete dataset test passed")
    
    def test_08_unauthorized_access(self):
        """Test unauthorized API access"""
        response = self.client.get('/api/v1/analytics/csv/datasets/')
        self.assertEqual(response.status_code, 401)
        print("✓ Unauthorized access test passed")
    
    def test_09_register_new_user(self):
        """Test user registration"""
        response = self.client.post(
            '/api/v1/auth/register/',
            data={
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'newpass123'
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('user', data)
        self.assertEqual(data['user']['username'], 'newuser')
        print("✓ User registration test passed")
    
    def test_10_complete_workflow(self):
        """Test complete workflow from login to PDF"""
        print("\n=== Testing Complete Workflow ===")
        
        # 1. Login
        login_response = self.client.post(
            '/api/v1/auth/login/',
            data={'username': 'testuser', 'password': 'testpass123'},
            content_type='application/json'
        )
        self.assertEqual(login_response.status_code, 200)
        print("1. ✓ Login successful")
        
        # 2. Upload CSV
        csv_content = b"""equipment name,type,flowrate,pressure,temperature
Reactor X,Reactor,155.2,10.8,87.1
Pump Y,Pump,205.5,16.2,46.8
Mixer Z,Mixer,175.8,11.5,52.3
Tank W,Tank,140.2,9.5,35.7"""
        
        csv_file = SimpleUploadedFile(
            "workflow_test.csv",
            csv_content,
            content_type="text/csv"
        )
        
        upload_response = self.client.post(
            '/api/v1/analytics/csv/upload/',
            {'file': csv_file},
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(upload_response.status_code, 200)
        dataset_id = upload_response.json()['dataset_id']
        print("2. ✓ CSV uploaded successfully")
        
        # 3. Get Statistics
        stats_response = self.client.get(
            '/api/v1/analytics/csv/statistics/',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(stats_response.status_code, 200)
        stats = stats_response.json()
        self.assertEqual(stats['total_equipment_count'], 4)
        print("3. ✓ Statistics retrieved successfully")
        
        # 4. List Datasets
        list_response = self.client.get(
            '/api/v1/analytics/csv/datasets/',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(list_response.status_code, 200)
        print("4. ✓ Datasets listed successfully")
        
        # 5. Generate PDF
        pdf_response = self.client.get(
            f'/api/v1/analytics/csv/datasets/{dataset_id}/pdf/',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(pdf_response.status_code, 200)
        self.assertGreater(len(pdf_response.content), 5000)  # PDF should be substantial
        print("5. ✓ PDF generated successfully")
        
        print("=== Complete Workflow Test PASSED ===\n")


def run_tests():
    """Helper function to run tests"""
    import sys
    from django.core.management import call_command
    
    print("\n" + "="*60)
    print("RUNNING COMPREHENSIVE APPLICATION TESTS")
    print("="*60 + "\n")
    
    # Run tests
    call_command('test', 'tests.test_complete_flow', verbosity=2)

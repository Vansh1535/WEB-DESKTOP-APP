"""
API Client for communicating with Django backend
"""

import requests
import json
import base64
from typing import Optional, Dict, Any, Tuple
from utils.config import Config

class APIClient:
    """Handles all API communications with the backend"""
    
    def __init__(self):
        self.base_url = Config.API_BASE_URL
        self.timeout = Config.API_TIMEOUT
        self.username = None
        self.password = None
        self.auth_header = None
    
    def set_credentials(self, username: str, password: str):
        """Set authentication credentials"""
        self.username = username
        self.password = password
        credentials = f"{username}:{password}"
        self.auth_header = base64.b64encode(credentials.encode()).decode()
    
    def clear_credentials(self):
        """Clear authentication credentials"""
        self.username = None
        self.password = None
        self.auth_header = None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        headers = {
            'Content-Type': 'application/json',
        }
        if self.auth_header:
            headers['Authorization'] = f'Basic {self.auth_header}'
        return headers
    
    def _handle_response(self, response: requests.Response) -> Tuple[bool, Any]:
        """Handle API response"""
        try:
            if response.status_code in [200, 201]:
                return True, response.json()
            else:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('error', f'Request failed with status {response.status_code}')
                return False, error_msg
        except Exception as e:
            return False, str(e)
    
    # Authentication APIs
    
    def login(self, username: str, password: str) -> Tuple[bool, Any]:
        """Login user"""
        try:
            url = f"{self.base_url}/api/v1/auth/login/"
            data = {
                'username': username,
                'password': password
            }
            response = requests.post(url, json=data, timeout=self.timeout)
            
            if response.status_code == 200:
                self.set_credentials(username, password)
                return True, response.json()
            else:
                error_data = response.json() if response.text else {}
                return False, error_data.get('error', 'Login failed')
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def register(self, username: str, email: str, password: str, 
                 first_name: str = "", last_name: str = "") -> Tuple[bool, Any]:
        """Register new user"""
        try:
            url = f"{self.base_url}/api/v1/auth/register/"
            data = {
                'username': username,
                'email': email,
                'password': password,
                'first_name': first_name,
                'last_name': last_name
            }
            response = requests.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def get_user_profile(self) -> Tuple[bool, Any]:
        """Get user profile"""
        try:
            url = f"{self.base_url}/api/v1/auth/profile/"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    # Dataset APIs
    
    def upload_csv(self, file_path: str) -> Tuple[bool, Any]:
        """Upload CSV file"""
        try:
            url = f"{self.base_url}/api/v1/analytics/csv/upload/"
            headers = {}
            if self.auth_header:
                headers['Authorization'] = f'Basic {self.auth_header}'
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files, headers=headers, 
                                       timeout=self.timeout)
            
            return self._handle_response(response)
        except Exception as e:
            return False, f"Upload error: {str(e)}"
    
    def list_datasets(self) -> Tuple[bool, Any]:
        """List all datasets"""
        try:
            url = f"{self.base_url}/api/v1/analytics/datasets/"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def get_dataset(self, dataset_id: int) -> Tuple[bool, Any]:
        """Get specific dataset details"""
        try:
            url = f"{self.base_url}/api/v1/analytics/datasets/{dataset_id}/"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def get_dataset_statistics(self, dataset_id: int) -> Tuple[bool, Any]:
        """Get dataset statistics"""
        try:
            url = f"{self.base_url}/api/v1/analytics/datasets/{dataset_id}/statistics/"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def get_dataset_data(self, dataset_id: int) -> Tuple[bool, Any]:
        """Get dataset raw data"""
        try:
            url = f"{self.base_url}/api/v1/analytics/datasets/{dataset_id}/data/"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def delete_dataset(self, dataset_id: int) -> Tuple[bool, Any]:
        """Delete a dataset"""
        try:
            url = f"{self.base_url}/api/v1/analytics/datasets/{dataset_id}/"
            headers = self._get_headers()
            response = requests.delete(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 204:
                return True, "Dataset deleted successfully"
            return self._handle_response(response)
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def get_statistics(self) -> Tuple[bool, Any]:
        """Get latest statistics"""
        try:
            url = f"{self.base_url}/api/v1/analytics/csv/statistics/"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def download_pdf_report(self, dataset_id: int, output_path: str) -> Tuple[bool, Any]:
        """Download PDF report for a dataset"""
        try:
            url = f"{self.base_url}/api/v1/analytics/datasets/{dataset_id}/pdf-report/"
            headers = {}
            if self.auth_header:
                headers['Authorization'] = f'Basic {self.auth_header}'
            
            response = requests.get(url, headers=headers, timeout=self.timeout, stream=True)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True, output_path
            else:
                return False, f"Failed to download PDF: {response.status_code}"
        except Exception as e:
            return False, f"Download error: {str(e)}"
    
    # User Preferences APIs
    
    def get_user_preferences(self) -> Tuple[bool, Any]:
        """Get user preferences"""
        try:
            url = f"{self.base_url}/api/v1/auth/preferences/"
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def update_user_preferences(self, preferences: Dict[str, Any]) -> Tuple[bool, Any]:
        """Update user preferences"""
        try:
            url = f"{self.base_url}/api/v1/auth/preferences/"
            headers = self._get_headers()
            response = requests.put(url, json=preferences, headers=headers, 
                                   timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            return False, f"Connection error: {str(e)}"

# Global API client instance
api_client = APIClient()

/**
 * API Service for connecting to Django Backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Store credentials in memory for Basic Auth
let authCredentials: string | null = null;

// TypeScript Interfaces
export interface UserPreferences {
  theme: 'light' | 'dark';
  default_view: 'charts' | 'data' | 'history';
  items_per_page: number;
  default_sort_column: string;
  default_sort_order: 'asc' | 'desc';
  last_active_dataset_id: number | null;
  updated_at: string;
}

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  date_joined: string;
  last_login: string;
  preferences: UserPreferences;
  upload_count: number;
}

/**
 * Set authentication credentials for API requests
 */
export function setAuthCredentials(username: string, password: string) {
  authCredentials = btoa(`${username}:${password}`);
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_credentials', authCredentials);
  }
}

/**
 * Get stored authentication credentials
 */
export function getAuthCredentials(): string | null {
  if (authCredentials) return authCredentials;
  
  if (typeof window !== 'undefined') {
    authCredentials = localStorage.getItem('auth_credentials');
  }
  
  return authCredentials;
}

/**
 * Clear authentication credentials
 */
export function clearAuthCredentials() {
  authCredentials = null;
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_credentials');
    localStorage.removeItem('user_data');
  }
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  return getAuthCredentials() !== null;
}

/**
 * Make authenticated API request
 */
async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const credentials = getAuthCredentials();
  
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };

  if (credentials) {
    headers['Authorization'] = `Basic ${credentials}`;
  }

  // Don't set Content-Type for FormData
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: 'include', // Important for session cookies
  });

  return response;
}

/**
 * Login user
 */
export async function login(username: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({ username, password }),
  });

  if (response.ok) {
    const data = await response.json();
    setAuthCredentials(username, password);
    
    if (typeof window !== 'undefined') {
      localStorage.setItem('user_data', JSON.stringify(data.user));
    }
    
    return { success: true, user: data.user };
  } else {
    const error = await response.json();
    return { success: false, error: error.error || 'Login failed' };
  }
}

/**
 * Register new user
 */
export async function register(
  username: string, 
  email: string,
  password: string,
  firstName?: string,
  lastName?: string
) {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/register/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({ 
      username, 
      email,
      password,
      first_name: firstName || '',
      last_name: lastName || ''
    }),
  });

  if (response.ok) {
    const data = await response.json();
    setAuthCredentials(username, password);
    
    if (typeof window !== 'undefined') {
      localStorage.setItem('user_data', JSON.stringify(data.user));
    }
    
    return { success: true, user: data.user };
  } else {
    const error = await response.json();
    return { success: false, error: error.error || 'Registration failed' };
  }
}

/**
 * Logout user
 */
export async function logout() {
  try {
    await apiRequest('/api/v1/auth/logout/', {
      method: 'POST',
    });
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    clearAuthCredentials();
  }
}

/**
 * Get current user data
 */
export function getCurrentUser() {
  if (typeof window === 'undefined') return null;
  
  const userData = localStorage.getItem('user_data');
  return userData ? JSON.parse(userData) : null;
}

/**
 * Get user profile with statistics
 */
export async function getUserProfile() {
  const response = await apiRequest('/api/v1/auth/profile/', {
    method: 'GET',
  });

  if (response.ok) {
    const data: UserProfile = await response.json();
    // Update local storage with fresh data
    if (typeof window !== 'undefined') {
      localStorage.setItem('user_data', JSON.stringify(data));
    }
    return { success: true, data };
  } else {
    const error = await response.json();
    return { success: false, error: error.error || 'Failed to fetch profile' };
  }
}

/**
 * Get user preferences
 */
export async function getUserPreferences() {
  const response = await apiRequest('/api/v1/auth/preferences/', {
    method: 'GET',
  });

  if (response.ok) {
    const data: UserPreferences = await response.json();
    return { success: true, data };
  } else {
    const error = await response.json();
    return { success: false, error: error.error || 'Failed to fetch preferences' };
  }
}

/**
 * Update user preferences
 */
export async function updateUserPreferences(preferences: Partial<UserPreferences>) {
  const response = await apiRequest('/api/v1/auth/preferences/', {
    method: 'PATCH',
    body: JSON.stringify(preferences),
  });

  if (response.ok) {
    const data: UserPreferences = await response.json();
    return { success: true, data };
  } else {
    const error = await response.json();
    return { success: false, error: error.error || 'Failed to update preferences' };
  }
}

/**
 * Upload CSV file
 */
export async function uploadCSV(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiRequest('/api/v1/analytics/csv/upload/', {
    method: 'POST',
    body: formData,
  });

  if (response.ok) {
    const data = await response.json();
    return { success: true, data };
  } else {
    const error = await response.json();
    return { 
      success: false, 
      error: error.error || error.details || 'Upload failed' 
    };
  }
}

/**
 * List all datasets
 */
export async function listDatasets() {
  const response = await apiRequest('/api/v1/analytics/csv/datasets/', {
    method: 'GET',
  });

  if (response.ok) {
    const data = await response.json();
    return { success: true, data };
  } else {
    const error = await response.json();
    return { success: false, error: error.error || 'Failed to fetch datasets' };
  }
}

/**
 * Get specific dataset
 */
export async function getDataset(id: number) {
  const response = await apiRequest(`/api/v1/analytics/csv/datasets/${id}/`, {
    method: 'GET',
  });

  if (response.ok) {
    const data = await response.json();
    return { success: true, data };
  } else {
    const error = await response.json();
    return { success: false, error: error.error || 'Failed to fetch dataset' };
  }
}

/**
 * Delete dataset
 */
export async function deleteDataset(id: number) {
  const response = await apiRequest(`/api/v1/analytics/csv/datasets/${id}/`, {
    method: 'DELETE',
  });

  if (response.ok) {
    const data = await response.json();
    return { success: true, message: data.message };
  } else {
    const error = await response.json();
    return { success: false, error: error.error || 'Failed to delete dataset' };
  }
}

/**
 * Get statistics from most recent dataset
 */
export async function getStatistics() {
  const response = await apiRequest('/api/v1/analytics/csv/statistics/', {
    method: 'GET',
  });

  if (response.ok) {
    const data = await response.json();
    return { success: true, data };
  } else {
    const error = await response.json();
    return { 
      success: false, 
      error: error.error || 'No statistics available' 
    };
  }
}

/**
 * Generate PDF report for a dataset
 */
export async function generatePDF(id: number) {
  const response = await apiRequest(`/api/v1/analytics/csv/datasets/${id}/pdf/`, {
    method: 'GET',
  });

  if (response.ok) {
    const blob = await response.blob();
    return { success: true, blob };
  } else {
    const error = await response.json();
    return { 
      success: false, 
      error: error.error || 'Failed to generate PDF' 
    };
  }
}

/**
 * Download PDF report
 */
export async function downloadPDF(id: number, filename: string = 'equipment_report.pdf') {
  const result = await generatePDF(id);
  
  if (result.success && result.blob) {
    const url = window.URL.createObjectURL(result.blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    return { success: true };
  }
  
  return result;
}

/**
 * Parse CSV data from backend response for frontend display
 */
export function parseBackendData(statistics: any): any[] {
  if (!statistics || !statistics.by_type) return [];
  
  const data: any[] = [];
  
  // Convert backend statistics back to row format for display
  Object.entries(statistics.by_type).forEach(([type, stats]: [string, any]) => {
    // Add sample rows for each type
    for (let i = 0; i < Math.min(stats.count, 3); i++) {
      data.push({
        equipment_name: `${type} ${i + 1}`,
        type: type,
        flowrate: stats.flowrate.avg,
        pressure: stats.pressure.avg,
        temperature: stats.temperature.avg,
      });
    }
  });
  
  return data;
}

export interface Dataset {
  id: number;
  file_name: string;
  uploaded_at: string;
  row_count: number;
  status: 'processing' | 'completed' | 'failed';
  statistics: any;
  uploaded_by_username: string;
}

export interface Statistics {
  total_equipment_count: number;
  by_type: {
    [key: string]: {
      count: number;
      flowrate: { avg: number; min: number; max: number };
      pressure: { avg: number; min: number; max: number };
      temperature: { avg: number; min: number; max: number };
    };
  };
  overall_averages: {
    flowrate: number;
    pressure: number;
    temperature: number;
  };
}

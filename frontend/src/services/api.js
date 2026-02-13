// API configuration and axios instance
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// API endpoints
export const authAPI = {
  login: (credentials) => api.post('/api/v1/auth/login', credentials),
  refresh: (refreshToken) => api.post('/api/v1/auth/refresh', { refresh_token: refreshToken }),
};

export const dashboardAPI = {
  getMetrics: (params) => api.get('/api/v1/dashboard/metrics', { params }),
  getMovementDetails: (params) => api.get('/api/v1/dashboard/movement-details', { params }),
};

export const purchasesAPI = {
  list: (params) => api.get('/api/v1/purchases', { params }),
  get: (id) => api.get(`/api/v1/purchases/${id}`),
  create: (data) => api.post('/api/v1/purchases', data),
  delete: (id) => api.delete(`/api/v1/purchases/${id}`),
};

export const transfersAPI = {
  list: (params) => api.get('/api/v1/transfers', { params }),
  get: (id) => api.get(`/api/v1/transfers/${id}`),
  create: (data) => api.post('/api/v1/transfers', data),
  updateStatus: (id, data) => api.put(`/api/v1/transfers/${id}`, data),
  delete: (id) => api.delete(`/api/v1/transfers/${id}`),
};

export const categoriesAPI = {
  list: () => api.get('/api/v1/categories'),
};

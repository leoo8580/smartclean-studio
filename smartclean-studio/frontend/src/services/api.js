import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000
});

export const uploadDataset = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const configureCleaning = async (sessionId, autoClean, operations = []) => {
  const response = await api.post('/configure', {
    session_id: sessionId,
    auto_clean: autoClean,
    operations: operations
  });
  return response.data;
};

export const applyCleaning = async (sessionId) => {
  const response = await api.post(`/clean?session_id=${sessionId}`);
  return response.data;
};

export const getReport = async (sessionId) => {
  const response = await api.get(`/report/${sessionId}`);
  return response.data;
};

export const getDataPreview = async (sessionId, limit = 100) => {
  const response = await api.get(`/preview/${sessionId}?limit=${limit}`);
  return response.data;
};

export const downloadData = async (sessionId, format) => {
  try {
    const response = await api.post(`/download/${sessionId}/${format}`, {}, {
      responseType: 'blob'
    });
    
    if (!response.data || response.data.size === 0) {
      throw new Error('Empty file received');
    }
    
    const url = URL.createObjectURL(response.data);
    const link = document.createElement('a');
    link.href = url;
    link.download = format === 'csv' ? 'cleaned_data.csv' : 'cleaned_data.xlsx';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    return true;
  } catch (error) {
    console.error('Download failed:', error);
    throw error;
  }
};

export default api;

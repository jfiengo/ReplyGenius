import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const businessApi = {
  register: (data) => api.post('/register-business', data),
  provisionNumber: (data) => api.post('/provision-number', data),
};

export const messageApi = {
  getHistory: (phoneNumber) => api.get(`/message-history/${phoneNumber}`),
};

export const contextApi = {
  upload: (formData) => api.post('/upload-context', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
};

export default api; 
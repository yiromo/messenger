import axios from 'axios';
import { getCookie } from 'cookies-next';

const api = axios.create({
  baseURL: 'http://localhost:8100',
});

api.interceptors.request.use((config) => {
  const token = getCookie('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

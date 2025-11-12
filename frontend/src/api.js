import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api', // This will be proxied by Nginx to the backend service in production
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to handle API errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // You can add more robust error handling here, e.g., for auth errors
    const message = error.response?.data?.detail || error.message;
    console.error('API Error:', message);
    // Optionally, show a notification to the user
    return Promise.reject(error);
  }
);

export const getAccounts = () => apiClient.get('/accounts');
export const addAccount = (username, password) => apiClient.post('/accounts', { username, password });
export const loginAccount = (username) => apiClient.post(`/accounts/${username}/login`);
export const updateAccountSettings = (username, settings) => apiClient.put(`/accounts/${username}/settings`, settings);
export const startTasks = (username) => apiClient.post(`/accounts/${username}/tasks/start`);
export const stopTasks = (username) => apiClient.post(`/accounts/${username}/tasks/stop`);
export const updateAccountTasks = (username, tasks) => apiClient.put(`/accounts/${username}/tasks`, { tasks });
export const getLogs = () => apiClient.get('/logs');

export default apiClient;

import axios from 'axios';

// Map this to your local backend server IP if running on device
// Or 10.0.2.2 if running on Android Emulator
const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

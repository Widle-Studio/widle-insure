import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const checkBackEndHealth = async () => {
    try {
        const response = await apiClient.get('/health');
        return response.data;
    } catch (error) {
        console.error("Backend health check failed:", error);
        return { status: "error", service: "widle-insure-backend" };
    }
};

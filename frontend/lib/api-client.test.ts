import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';

// Mock axios module completely
vi.mock('axios', () => {
  return {
    default: {
      create: vi.fn(() => ({
        get: vi.fn(),
      })),
    },
  };
});

// We need to import the module *after* defining the mock.
import { apiClient, checkBackEndHealth } from './api-client';

describe('api-client', () => {
  let mockGet: any;

  beforeEach(() => {
    // Note: Do NOT clear axios.create mock history here, because it gets called
    // ONCE when `api-client.ts` is imported, which is outside the `it` blocks.
    // If we clear it here, the test asserting it was called will fail!
    mockGet = (apiClient as any).get;
    mockGet.mockClear();
  });

  describe('apiClient instance', () => {
    it('creates an axios instance with the correct default configuration', () => {
      expect(axios.create).toHaveBeenCalledWith({
        baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
        headers: {
          'Content-Type': 'application/json',
        },
      });
    });
  });

  describe('checkBackEndHealth', () => {
    it('returns response data on successful health check', async () => {
      const mockData = { status: 'ok', service: 'widle-insure-backend' };
      mockGet.mockResolvedValueOnce({ data: mockData });

      const result = await checkBackEndHealth();

      expect(mockGet).toHaveBeenCalledWith('/health');
      expect(result).toEqual(mockData);
    });

    it('returns an error object when the health check fails', async () => {
      const mockError = new Error('Network Error');
      mockGet.mockRejectedValueOnce(mockError);

      // Spy on console.error to prevent actual logging during tests and to assert it was called
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      const result = await checkBackEndHealth();

      expect(mockGet).toHaveBeenCalledWith('/health');
      expect(consoleSpy).toHaveBeenCalledWith("Backend health check failed:", mockError);
      expect(result).toEqual({ status: "error", service: "widle-insure-backend" });

      consoleSpy.mockRestore();
    });
  });
});

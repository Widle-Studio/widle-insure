import { checkBackEndHealth, apiClient } from './api-client';
import MockAdapter from 'axios-mock-adapter';

describe('api-client', () => {
    let mock: MockAdapter;

    beforeAll(() => {
        mock = new MockAdapter(apiClient);
        // Suppress console.error during tests to keep output clean
        jest.spyOn(console, 'error').mockImplementation(() => {});
    });

    afterEach(() => {
        mock.reset();
    });

    afterAll(() => {
        mock.restore();
        jest.restoreAllMocks();
    });

    describe('checkBackEndHealth', () => {
        it('should return health status successfully', async () => {
            const mockData = { status: 'ok', service: 'widle-insure-backend' };
            mock.onGet('/health').reply(200, mockData);

            const result = await checkBackEndHealth();

            expect(result).toEqual(mockData);
        });

        it('should return error status when the request fails (e.g. 500)', async () => {
            mock.onGet('/health').reply(500);

            const result = await checkBackEndHealth();

            expect(result).toEqual({ status: 'error', service: 'widle-insure-backend' });
            expect(console.error).toHaveBeenCalledWith(
                'Backend health check failed:',
                expect.any(Error)
            );
        });

        it('should return error status on network error', async () => {
            mock.onGet('/health').networkError();

            const result = await checkBackEndHealth();

            expect(result).toEqual({ status: 'error', service: 'widle-insure-backend' });
            expect(console.error).toHaveBeenCalledWith(
                'Backend health check failed:',
                expect.any(Error)
            );
        });
    });
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

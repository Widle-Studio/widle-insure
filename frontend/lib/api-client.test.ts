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
});

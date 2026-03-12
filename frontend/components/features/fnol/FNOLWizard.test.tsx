import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import { FNOLWizard } from './FNOLWizard';
import { apiClient } from '@/lib/api-client';
import { useRouter } from 'next/navigation';

// Mock Next.js router
jest.mock('next/navigation', () => ({
    useRouter: jest.fn(),
}));

// Mock api client
jest.mock('../../../lib/api-client', () => ({
    apiClient: {
        post: jest.fn(),
    },
}));

// Mock framer-motion to avoid animation issues in tests
jest.mock('framer-motion', () => ({
    motion: {
        div: ({ children, ...props }: any) => {
            const { initial, animate, exit, transition, ...rest } = props;
            return <div {...rest}>{children}</div>;
        },
    },
    AnimatePresence: ({ children }: any) => <>{children}</>,
}));

describe('FNOLWizard', () => {
    const mockRouterPush = jest.fn();

    beforeEach(() => {
        jest.clearAllMocks();
        (useRouter as jest.Mock).mockReturnValue({
            push: mockRouterPush,
        });
    });

    const fillStep1 = async (user: ReturnType<typeof userEvent.setup>) => {
        await user.type(screen.getByLabelText('Policy Number'), 'POL-123456');
        await user.type(screen.getByLabelText('Full Name'), 'John Doe');
        await user.type(screen.getByLabelText('Email'), 'john@example.com');
        await user.type(screen.getByLabelText('Phone'), '555-0123');
    };

    const fillStep2 = async (user: ReturnType<typeof userEvent.setup>) => {
        // Find input datetime-local by label might be tricky if not perfectly mapped, so using label text or getByRole
        // Let's use getByLabelText based on Step2Incident
        await user.type(screen.getByLabelText('Date & Time'), '2023-10-25T14:30');
        await user.type(screen.getByLabelText('Location'), '123 Main St');
        await user.type(screen.getByLabelText('Description'), 'Rear-ended at stoplight');
    };

    const fillStep3 = async (user: ReturnType<typeof userEvent.setup>) => {
        await user.type(screen.getByLabelText('Year'), '2022');
        await user.type(screen.getByLabelText('Make'), 'Toyota');
        await user.type(screen.getByLabelText('Model'), 'Camry');
    };

    it('renders the first step initially', () => {
        render(<FNOLWizard />);
        expect(screen.getByText('File a New Claim')).toBeInTheDocument();
        expect(screen.getByText('Step 1 of 4')).toBeInTheDocument();
        expect(screen.getByLabelText('Policy Number')).toBeInTheDocument();
    });

    it('allows navigating forward and backward', async () => {
        const user = userEvent.setup();
        render(<FNOLWizard />);

        // Fill step 1
        await fillStep1(user);

        // Click next
        await user.click(screen.getByRole('button', { name: /next/i }));

        // Wait for step 2 to render
        await waitFor(() => {
            expect(screen.getByText('Step 2 of 4')).toBeInTheDocument();
            expect(screen.getByLabelText('Date & Time')).toBeInTheDocument();
        });

        // Click back
        await user.click(screen.getByRole('button', { name: /back/i }));

        // Wait for step 1 to render again
        await waitFor(() => {
            expect(screen.getByText('Step 1 of 4')).toBeInTheDocument();
            expect(screen.getByLabelText('Policy Number')).toBeInTheDocument();
        });
    });

    it('validates fields before proceeding', async () => {
        const user = userEvent.setup();
        render(<FNOLWizard />);

        // Click next without filling fields
        await user.click(screen.getByRole('button', { name: /next/i }));

        // Wait for error messages
        await waitFor(() => {
            expect(screen.getByText('Step 1 of 4')).toBeInTheDocument(); // should not proceed
        });
    });

    it('submits the form successfully and redirects', async () => {
        const user = userEvent.setup();
        const mockPost = apiClient.post as jest.Mock;
        mockPost.mockResolvedValueOnce({ data: { id: 'claim-123' } }); // Mock claim creation

        render(<FNOLWizard />);

        // Step 1
        await fillStep1(user);
        await user.click(screen.getByRole('button', { name: /next/i }));

        // Step 2
        await waitFor(() => screen.getByLabelText('Date & Time'));
        await fillStep2(user);
        await user.click(screen.getByRole('button', { name: /next/i }));

        // Step 3
        await waitFor(() => screen.getByLabelText('Year'));
        await fillStep3(user);
        await user.click(screen.getByRole('button', { name: /next/i }));

        // Step 4 (Photos)
        await waitFor(() => screen.getByText('Step 4 of 4'));

        // Mock a file upload by calling the upload logic or just skipping file upload for this test
        // Let's test the submit button directly
        const submitButton = screen.getByRole('button', { name: /submit claim/i });
        await user.click(submitButton);

        await waitFor(() => {
            expect(mockPost).toHaveBeenCalledTimes(1);
            expect(mockPost).toHaveBeenCalledWith('/api/v1/claims', expect.objectContaining({
                policy_number: 'POL-123456',
                claimant_name: 'John Doe',
                claimant_email: 'john@example.com',
                claimant_phone: '555-0123',
                incident_date: '2023-10-25T14:30',
                incident_location: '123 Main St',
                incident_description: 'Rear-ended at stoplight',
                vehicle_year: 2022,
                vehicle_make: 'Toyota',
                vehicle_model: 'Camry',
            }));
            expect(mockRouterPush).toHaveBeenCalledWith('/?claim_id=claim-123&status=submitted');
        });
    });

    it('handles submission errors', async () => {
        const user = userEvent.setup();
        const mockPost = apiClient.post as jest.Mock;
        mockPost.mockRejectedValueOnce(new Error('Network error'));

        const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});

        render(<FNOLWizard />);

        // Step 1
        await fillStep1(user);
        await user.click(screen.getByRole('button', { name: /next/i }));

        // Step 2
        await waitFor(() => screen.getByLabelText('Date & Time'));
        await fillStep2(user);
        await user.click(screen.getByRole('button', { name: /next/i }));

        // Step 3
        await waitFor(() => screen.getByLabelText('Year'));
        await fillStep3(user);
        await user.click(screen.getByRole('button', { name: /next/i }));

        // Step 4
        await waitFor(() => screen.getByText('Step 4 of 4'));

        await user.click(screen.getByRole('button', { name: /submit claim/i }));

        await waitFor(() => {
            expect(mockPost).toHaveBeenCalledTimes(1);
            expect(alertMock).toHaveBeenCalledWith('Failed to submit claim. Please try again.');
            expect(mockRouterPush).not.toHaveBeenCalled();
        });

        alertMock.mockRestore();
    });
});

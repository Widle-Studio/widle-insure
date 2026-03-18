import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import { FNOLWizard } from './FNOLWizard';
import { apiClient } from '@/lib/api-client';

// Mock useRouter
const mockPush = jest.fn();
jest.mock('next/navigation', () => ({
    useRouter: () => ({
        push: mockPush,
    }),
}));

// Mock API Client
jest.mock('@/lib/api-client', () => ({
    apiClient: {
        post: jest.fn(),
    },
}));

// Mock framer-motion to bypass animations
jest.mock('framer-motion', () => {
    const ActualFramerMotion = jest.requireActual('framer-motion');
    return {
        ...ActualFramerMotion,
        AnimatePresence: ({ children }: any) => <>{children}</>,
        motion: {
            ...ActualFramerMotion.motion,
            div: ({ children, ...props }: any) => {
                // Filter out framer-motion specific props to avoid React warnings on DOM elements
                const { initial, animate, exit, transition, ...validProps } = props;
                return <div {...validProps}>{children}</div>;
            },
        },
    };
});

// Mock window.alert
const mockAlert = jest.fn();
window.alert = mockAlert;

describe('FNOLWizard Integration Tests', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    const fillStep1 = async (user: any) => {
        await user.type(screen.getByLabelText('Policy Number'), 'POL-123456');
        await user.type(screen.getByLabelText('Full Name'), 'John Doe');
        await user.type(screen.getByLabelText('Email'), 'john@example.com');
        await user.type(screen.getByLabelText('Phone'), '555-0123');
        await user.click(screen.getByRole('button', { name: 'Next' }));
    };

    const fillStep2 = async (user: any) => {
        // Find by label text or placeholder
        await user.type(screen.getByLabelText('Date & Time'), '2023-10-27T10:30');
        await user.type(screen.getByLabelText('Location'), '123 Main St');
        await user.type(screen.getByLabelText('Description'), 'Rear-ended at a stoplight');
        await user.click(screen.getByRole('button', { name: 'Next' }));
    };

    const fillStep3 = async (user: any) => {
        await user.type(screen.getByLabelText('Year'), '2022');
        await user.type(screen.getByLabelText('Make'), 'Toyota');
        await user.type(screen.getByLabelText('Model'), 'Camry');
        await user.type(screen.getByLabelText('VIN (Optional)'), '1HGCM82633A00000');
        await user.click(screen.getByRole('button', { name: 'Next' }));
    };

    it('successfully submits the form when all required fields are valid', async () => {
        const user = userEvent.setup();
        (apiClient.post as jest.Mock).mockResolvedValueOnce({ data: { id: 'claim-123' } });

        render(<FNOLWizard />);

        // Step 1
        await fillStep1(user);

        // Step 2
        await fillStep2(user);

        // Step 3
        await fillStep3(user);

        // Step 4 (Photos) - Skip photos and submit
        await user.click(screen.getByRole('button', { name: 'Submit Claim' }));

        await waitFor(() => {
            expect(apiClient.post).toHaveBeenCalledTimes(1);
        });

        expect(apiClient.post).toHaveBeenCalledWith('/api/v1/claims', {
            policy_number: 'POL-123456',
            claimant_name: 'John Doe',
            claimant_email: 'john@example.com',
            claimant_phone: '555-0123',
            incident_date: '2023-10-27T10:30',
            incident_location: '123 Main St',
            incident_description: 'Rear-ended at a stoplight',
            vehicle_year: 2022,
            vehicle_make: 'Toyota',
            vehicle_model: 'Camry',
            vehicle_vin: '1HGCM82633A00000',
        });

        expect(mockPush).toHaveBeenCalledWith('/?claim_id=claim-123&status=submitted');
    });

    it('prevents navigation to next step if validation fails', async () => {
        const user = userEvent.setup();
        render(<FNOLWizard />);

        // Try to click Next on Step 1 without filling anything
        await user.click(screen.getByRole('button', { name: 'Next' }));

        // Ensure we are still on Step 1 (Policy Number field still visible)
        expect(screen.getByLabelText('Policy Number')).toBeInTheDocument();

        // Validation error messages should appear
        expect(await screen.findByText('Policy number is required')).toBeInTheDocument();
        expect(await screen.findByText('Name is required')).toBeInTheDocument();
        expect(await screen.findByText('Email is required')).toBeInTheDocument();
        expect(await screen.findByText('Phone is required')).toBeInTheDocument();
    });

    it('allows navigating back to previous steps', async () => {
        const user = userEvent.setup();
        render(<FNOLWizard />);

        // Fill Step 1 and go to Step 2
        await fillStep1(user);

        // Ensure we are on Step 2
        expect(screen.getByLabelText('Date & Time')).toBeInTheDocument();

        // Click Back
        await user.click(screen.getByRole('button', { name: 'Back' }));

        // Ensure we are back on Step 1
        expect(screen.getByLabelText('Policy Number')).toBeInTheDocument();
        // Values should persist
        expect(screen.getByLabelText('Policy Number')).toHaveValue('POL-123456');
    });

    it('shows an alert if the API submission fails', async () => {
        const user = userEvent.setup();
        // Mock rejection for submission
        (apiClient.post as jest.Mock).mockRejectedValueOnce(new Error('API Error'));

        render(<FNOLWizard />);

        await fillStep1(user);
        await fillStep2(user);
        await fillStep3(user);

        await user.click(screen.getByRole('button', { name: 'Submit Claim' }));

        await waitFor(() => {
            expect(mockAlert).toHaveBeenCalledWith('Failed to submit claim. Please try again.');
        });
    });
});

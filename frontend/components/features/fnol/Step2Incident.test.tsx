import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { UseFormReturn } from 'react-hook-form';
import { Step2Incident } from './Step2Incident';
import { FNOLFormData } from '@/types/fnol';

describe('Step2Incident', () => {
    const mockRegister = jest.fn();

    const getMockForm = (errors = {}): UseFormReturn<FNOLFormData> => {
        return {
            register: mockRegister,
            formState: {
                errors,
            },
        } as unknown as UseFormReturn<FNOLFormData>;
    };

    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('renders all input fields correctly', () => {
        render(<Step2Incident form={getMockForm()} />);

        // Check for Date & Time
        expect(screen.getByLabelText('Date & Time')).toBeInTheDocument();

        // Check for Location
        expect(screen.getByLabelText('Location')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('123 Main St, Springfield')).toBeInTheDocument();

        // Check for Description
        expect(screen.getByLabelText('Description')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Describe what happened...')).toBeInTheDocument();
    });

    it('calls register function for all fields', () => {
        render(<Step2Incident form={getMockForm()} />);

        expect(mockRegister).toHaveBeenCalledWith('incident_date', { required: 'Date is required' });
        expect(mockRegister).toHaveBeenCalledWith('incident_location', { required: 'Location is required' });
        expect(mockRegister).toHaveBeenCalledWith('incident_description', { required: 'Description is required' });
    });

    it('displays error messages when they exist', () => {
        const errors = {
            incident_date: { type: 'required', message: 'Date is required' },
            incident_location: { type: 'required', message: 'Location is required' },
            incident_description: { type: 'required', message: 'Description is required' },
        };

        render(<Step2Incident form={getMockForm(errors)} />);

        expect(screen.getByText('Date is required')).toBeInTheDocument();
        expect(screen.getByText('Location is required')).toBeInTheDocument();
        expect(screen.getByText('Description is required')).toBeInTheDocument();
    });

    it('renders the card header correctly', () => {
        render(<Step2Incident form={getMockForm()} />);
        expect(screen.getByText('Incident Details')).toBeInTheDocument();
    });

    it('renders the date input with the correct type attribute', () => {
        render(<Step2Incident form={getMockForm()} />);
        const dateInput = screen.getByLabelText('Date & Time');
        expect(dateInput).toHaveAttribute('type', 'datetime-local');
    });

    it('renders correctly without errors object properties', () => {
        const { container } = render(<Step2Incident form={getMockForm({})} />);
        expect(container).toBeInTheDocument();

        // No error messages should be displayed
        expect(screen.queryByText('Date is required')).not.toBeInTheDocument();
        expect(screen.queryByText('Location is required')).not.toBeInTheDocument();
        expect(screen.queryByText('Description is required')).not.toBeInTheDocument();
    });

    it('matches the snapshot for Step2Incident', () => {
        const { asFragment } = render(<Step2Incident form={getMockForm()} />);
        expect(asFragment()).toMatchSnapshot();
    });
});

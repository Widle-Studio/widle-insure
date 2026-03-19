import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { UseFormReturn } from 'react-hook-form';
import { Step3Vehicle } from './Step3Vehicle';
import { FNOLFormData } from '@/types/fnol';

describe('Step3Vehicle', () => {
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
        render(<Step3Vehicle form={getMockForm()} />);

        // Check for Year
        expect(screen.getByLabelText('Year')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('2022')).toBeInTheDocument();

        // Check for Make
        expect(screen.getByLabelText('Make')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Toyota')).toBeInTheDocument();

        // Check for Model
        expect(screen.getByLabelText('Model')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Camry')).toBeInTheDocument();

        // Check for VIN
        expect(screen.getByLabelText('VIN (Optional)')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('XXXXXXXXXXXXXXXXX')).toBeInTheDocument();
    });

    it('calls register function for all fields', () => {
        render(<Step3Vehicle form={getMockForm()} />);

        expect(mockRegister).toHaveBeenCalledWith('vehicle_year', { required: 'Year is required', valueAsNumber: true });
        expect(mockRegister).toHaveBeenCalledWith('vehicle_make', { required: 'Make is required' });
        expect(mockRegister).toHaveBeenCalledWith('vehicle_model', { required: 'Model is required' });
        expect(mockRegister).toHaveBeenCalledWith('vehicle_vin');
    });

    it('displays error messages when they exist', () => {
        const errors = {
            vehicle_year: { type: 'required', message: 'Year is required' },
            vehicle_make: { type: 'required', message: 'Make is required' },
            vehicle_model: { type: 'required', message: 'Model is required' },
        };

        render(<Step3Vehicle form={getMockForm(errors)} />);

        expect(screen.getByText('Year is required')).toBeInTheDocument();
        expect(screen.getByText('Make is required')).toBeInTheDocument();
        expect(screen.getByText('Model is required')).toBeInTheDocument();
    });

    it('renders the card header correctly', () => {
        render(<Step3Vehicle form={getMockForm()} />);
        expect(screen.getByText('Vehicle Information')).toBeInTheDocument();
    });

    it('renders the year input with the correct type attribute', () => {
        render(<Step3Vehicle form={getMockForm()} />);
        const yearInput = screen.getByLabelText('Year');
        expect(yearInput).toHaveAttribute('type', 'number');
    });

    it('renders correctly without errors object properties', () => {
        const { container } = render(<Step3Vehicle form={getMockForm({})} />);
        expect(container).toBeInTheDocument();

        // No error messages should be displayed
        expect(screen.queryByText('Year is required')).not.toBeInTheDocument();
        expect(screen.queryByText('Make is required')).not.toBeInTheDocument();
        expect(screen.queryByText('Model is required')).not.toBeInTheDocument();
    });
});

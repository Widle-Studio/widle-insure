import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { UseFormReturn } from 'react-hook-form';
import { Step1Policy } from './Step1Policy';
import { FNOLFormData } from '@/types/fnol';

describe('Step1Policy', () => {
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
        render(<Step1Policy form={getMockForm()} />);

        // Check for Policy Number
        expect(screen.getByLabelText('Policy Number')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('POL-XXXXXXXX')).toBeInTheDocument();

        // Check for Full Name
        expect(screen.getByLabelText('Full Name')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('John Doe')).toBeInTheDocument();

        // Check for Email
        expect(screen.getByLabelText('Email')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('john@example.com')).toBeInTheDocument();

        // Check for Phone
        expect(screen.getByLabelText('Phone')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('555-0123')).toBeInTheDocument();
    });

    it('calls register function for all fields', () => {
        render(<Step1Policy form={getMockForm()} />);

        expect(mockRegister).toHaveBeenCalledWith('policy_number', { required: 'Policy number is required' });
        expect(mockRegister).toHaveBeenCalledWith('claimant_name', { required: 'Name is required' });
        expect(mockRegister).toHaveBeenCalledWith('claimant_email', { required: 'Email is required' });
        expect(mockRegister).toHaveBeenCalledWith('claimant_phone', { required: 'Phone is required' });
    });

    it('displays error messages when they exist', () => {
        const errors = {
            policy_number: { type: 'required', message: 'Policy number is required' },
            claimant_name: { type: 'required', message: 'Name is required' },
            claimant_email: { type: 'required', message: 'Email is required' },
            claimant_phone: { type: 'required', message: 'Phone is required' },
        };

        render(<Step1Policy form={getMockForm(errors)} />);

        expect(screen.getByText('Policy number is required')).toBeInTheDocument();
        expect(screen.getByText('Name is required')).toBeInTheDocument();
        expect(screen.getByText('Email is required')).toBeInTheDocument();
        expect(screen.getByText('Phone is required')).toBeInTheDocument();
    });

    it('renders the card header correctly', () => {
        render(<Step1Policy form={getMockForm()} />);
        expect(screen.getByText('Claimant & Policy Information')).toBeInTheDocument();
    });

    it('renders the email input with the correct type attribute', () => {
        render(<Step1Policy form={getMockForm()} />);
        const emailInput = screen.getByLabelText('Email');
        expect(emailInput).toHaveAttribute('type', 'email');
    });

    it('renders correctly without errors object properties', () => {
        const { container } = render(<Step1Policy form={getMockForm({})} />);
        expect(container).toBeInTheDocument();

        // No error messages should be displayed
        expect(screen.queryByText('Policy number is required')).not.toBeInTheDocument();
        expect(screen.queryByText('Name is required')).not.toBeInTheDocument();
        expect(screen.queryByText('Email is required')).not.toBeInTheDocument();
        expect(screen.queryByText('Phone is required')).not.toBeInTheDocument();
    });
});

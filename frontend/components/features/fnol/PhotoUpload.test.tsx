import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { PhotoUpload } from './PhotoUpload';

// Mock framer-motion to prevent animation issues in tests
jest.mock('framer-motion', () => {
    const ActualFramerMotion = jest.requireActual('framer-motion');
    return {
        ...ActualFramerMotion,
        motion: {
            div: ({ children, ...props }: any) => {
                const { initial, animate, exit, transition, ...validProps } = props;
                return <div {...validProps}>{children}</div>;
            },
        },
        AnimatePresence: ({ children }: any) => <>{children}</>,
    };
});

describe('PhotoUpload', () => {
    const mockOnPhotosSelected = jest.fn();
    let originalCreateObjectURL: typeof URL.createObjectURL;
    let originalRevokeObjectURL: typeof URL.revokeObjectURL;

    beforeAll(() => {
        // Mock URL object methods
        originalCreateObjectURL = URL.createObjectURL;
        originalRevokeObjectURL = URL.revokeObjectURL;

        URL.createObjectURL = jest.fn((file: File | Blob) => {
            return `blob:http://localhost/${file.name}`;
        });
        URL.revokeObjectURL = jest.fn();
    });

    afterAll(() => {
        // Restore original URL object methods
        URL.createObjectURL = originalCreateObjectURL;
        URL.revokeObjectURL = originalRevokeObjectURL;
    });

    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('renders correctly', () => {
        render(<PhotoUpload onPhotosSelected={mockOnPhotosSelected} />);

        expect(screen.getByText('Upload Damage Photos')).toBeInTheDocument();
        expect(screen.getByText('Click to upload or drag and drop')).toBeInTheDocument();
        expect(screen.getByText('SVG, PNG, JPG or GIF (max 5MB)')).toBeInTheDocument();
    });

    it('handles file selection and generates previews', async () => {
        render(<PhotoUpload onPhotosSelected={mockOnPhotosSelected} />);

        const file = new File(['dummy content'], 'test.png', { type: 'image/png' });
        const input = document.getElementById('photos') as HTMLInputElement;

        // Use fireEvent for file inputs to trigger onChange reliably
        fireEvent.change(input, { target: { files: [file] } });

        expect(mockOnPhotosSelected).toHaveBeenCalledWith([file]);
        expect(URL.createObjectURL).toHaveBeenCalledWith(file);

        // Wait for preview to render
        await waitFor(() => {
            const previewImage = screen.getByAltText('Preview 0');
            expect(previewImage).toBeInTheDocument();
            expect(previewImage).toHaveAttribute('src', 'blob:http://localhost/test.png');
        });
    });

    it('handles multiple file selection', async () => {
        render(<PhotoUpload onPhotosSelected={mockOnPhotosSelected} />);

        const file1 = new File(['dummy 1'], 'test1.png', { type: 'image/png' });
        const file2 = new File(['dummy 2'], 'test2.png', { type: 'image/png' });
        const input = document.getElementById('photos') as HTMLInputElement;

        fireEvent.change(input, { target: { files: [file1, file2] } });

        expect(mockOnPhotosSelected).toHaveBeenCalledWith([file1, file2]);
        expect(URL.createObjectURL).toHaveBeenCalledTimes(2);

        await waitFor(() => {
            expect(screen.getByAltText('Preview 0')).toBeInTheDocument();
            expect(screen.getByAltText('Preview 1')).toBeInTheDocument();
        });
    });

    it('handles removing a photo', async () => {
        render(<PhotoUpload onPhotosSelected={mockOnPhotosSelected} />);

        const file1 = new File(['dummy 1'], 'test1.png', { type: 'image/png' });
        const file2 = new File(['dummy 2'], 'test2.png', { type: 'image/png' });
        const input = document.getElementById('photos') as HTMLInputElement;

        // Add 2 files
        fireEvent.change(input, { target: { files: [file1, file2] } });

        // Verify they are added
        await waitFor(() => {
            expect(screen.getAllByRole('button').length).toBe(2); // Remove buttons
        });

        // Click remove on the first photo (index 0)
        const removeButtons = screen.getAllByRole('button');
        fireEvent.click(removeButtons[0]);

        // It should call onPhotosSelected with only the remaining file
        expect(mockOnPhotosSelected).toHaveBeenLastCalledWith([file2]);

        // It should revoke the object URL for the removed preview
        expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:http://localhost/test1.png');

        // Only one preview should remain
        await waitFor(() => {
            // Note: Since we removed index 0, the remaining one will be re-rendered with index 0
            expect(screen.getAllByRole('button').length).toBe(1);

            // Check the src of the remaining image
            const remainingImage = screen.getByAltText('Preview 0');
            expect(remainingImage).toHaveAttribute('src', 'blob:http://localhost/test2.png');
        });
    });

    it('triggers click on hidden file input when card is clicked', () => {
        render(<PhotoUpload onPhotosSelected={mockOnPhotosSelected} />);

        // Mock the click on the input element
        const input = document.getElementById('photos') as HTMLInputElement;
        const inputClickSpy = jest.spyOn(input, 'click');

        // Click the card
        const cardContent = screen.getByText('Click to upload or drag and drop').closest('div')?.parentElement;
        if (cardContent) {
            fireEvent.click(cardContent);
        }

        expect(inputClickSpy).toHaveBeenCalled();
    });
});

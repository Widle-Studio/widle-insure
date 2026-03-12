import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { PhotoUpload } from './PhotoUpload';

// Mock matchMedia for framer-motion or other components if necessary
window.matchMedia = window.matchMedia || function() {
  return {
    matches: false,
    addListener: function() {},
    removeListener: function() {}
  };
};

describe('PhotoUpload', () => {
    const mockOnPhotosSelected = jest.fn();

    beforeAll(() => {
        // Mock URL.createObjectURL and URL.revokeObjectURL
        global.URL.createObjectURL = jest.fn(() => 'blob:mock-url');
        global.URL.revokeObjectURL = jest.fn();
    });

    afterAll(() => {
        jest.restoreAllMocks();
    });

    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('renders the upload component correctly', () => {
        render(<PhotoUpload onPhotosSelected={mockOnPhotosSelected} />);

        expect(screen.getByText('Upload Damage Photos')).toBeInTheDocument();
        expect(screen.getByText(/Please upload clear photos of the damage/i)).toBeInTheDocument();
        expect(screen.getByText('Click to upload or drag and drop')).toBeInTheDocument();
    });

    it('handles file selection correctly', async () => {
        render(<PhotoUpload onPhotosSelected={mockOnPhotosSelected} />);

        const file = new File(['hello'], 'hello.png', { type: 'image/png' });
        const input = document.getElementById('photos') as HTMLInputElement;

        fireEvent.change(input, { target: { files: [file] } });

        expect(mockOnPhotosSelected).toHaveBeenCalledWith([file]);
        expect(global.URL.createObjectURL).toHaveBeenCalledWith(file);

        // Wait for preview to render
        await waitFor(() => {
            const previewImage = screen.getByAltText('Preview 0');
            expect(previewImage).toBeInTheDocument();
            expect(previewImage).toHaveAttribute('src', 'blob:mock-url');
        });
    });

    it('handles multiple file uploads sequentially', async () => {
        render(<PhotoUpload onPhotosSelected={mockOnPhotosSelected} />);

        const file1 = new File(['hello'], 'hello.png', { type: 'image/png' });
        const input = document.getElementById('photos') as HTMLInputElement;

        fireEvent.change(input, { target: { files: [file1] } });
        expect(mockOnPhotosSelected).toHaveBeenLastCalledWith([file1]);

        const file2 = new File(['world'], 'world.png', { type: 'image/png' });
        fireEvent.change(input, { target: { files: [file2] } });

        // Component should accumulate files
        expect(mockOnPhotosSelected).toHaveBeenLastCalledWith([file1, file2]);

        await waitFor(() => {
            expect(screen.getByAltText('Preview 0')).toBeInTheDocument();
            expect(screen.getByAltText('Preview 1')).toBeInTheDocument();
        });
    });

    it('removes a selected photo correctly', async () => {
        render(<PhotoUpload onPhotosSelected={mockOnPhotosSelected} />);

        const file1 = new File(['hello'], 'hello.png', { type: 'image/png' });
        const file2 = new File(['world'], 'world.png', { type: 'image/png' });
        const input = document.getElementById('photos') as HTMLInputElement;

        // Add two files
        fireEvent.change(input, { target: { files: [file1, file2] } });

        await waitFor(() => {
            expect(screen.getByAltText('Preview 0')).toBeInTheDocument();
            expect(screen.getByAltText('Preview 1')).toBeInTheDocument();
        });

        // Find remove buttons (we expect 2)
        const removeButtons = screen.getAllByRole('button');
        expect(removeButtons).toHaveLength(2);

        // Click remove button for the first preview
        fireEvent.click(removeButtons[0]);

        // revokeObjectURL should be called
        expect(global.URL.revokeObjectURL).toHaveBeenCalledWith('blob:mock-url');

        // onPhotosSelected should be called with only the second file
        expect(mockOnPhotosSelected).toHaveBeenLastCalledWith([file2]);

        // Only one preview should remain (the text might change to 0 if indexes are recalculated in map)
        await waitFor(() => {
             // In the component: `<img src={src} alt={\`Preview \${index}\`} />`
             // When we remove index 0, the remaining file becomes index 0 in the new array
             const images = screen.getAllByRole('img');
             expect(images).toHaveLength(1);
        });
    });
});

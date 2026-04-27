import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import LoginPage from "./page";
import { apiClient } from "@/lib/api-client";
import { useRouter } from "next/navigation";
import "@testing-library/jest-dom";

// Mock the dependencies
jest.mock("next/navigation", () => ({
    useRouter: jest.fn(),
}));

jest.mock("@/lib/api-client", () => ({
    apiClient: {
        get: jest.fn(),
    },
}));

describe("LoginPage", () => {
    const mockPush = jest.fn();

    beforeEach(() => {
        // Reset all mocks before each test
        jest.clearAllMocks();
        (useRouter as jest.Mock).mockReturnValue({
            push: mockPush,
        });
    });

    it("renders the login form correctly", () => {
        render(<LoginPage />);

        expect(screen.getByRole("heading", { name: "Sign in" })).toBeInTheDocument();
        expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
        expect(screen.getByRole("button", { name: "Sign In" })).toBeInTheDocument();
    });

    it("handles successful login when backend is healthy", async () => {
        // Mock healthy response
        (apiClient.get as jest.Mock).mockResolvedValueOnce({
            data: { status: "healthy" },
        });

        render(<LoginPage />);

        const user = userEvent.setup();
        await user.type(screen.getByLabelText(/email/i), "test@example.com");
        await user.type(screen.getByLabelText(/password/i), "password123");

        await user.click(screen.getByRole("button", { name: "Sign In" }));

        await waitFor(() => {
            expect(apiClient.get).toHaveBeenCalledWith("/health");
            expect(mockPush).toHaveBeenCalledWith("/dashboard");
        });
    });

    it("shows error when backend is not healthy", async () => {
        // Mock unhealthy response
        (apiClient.get as jest.Mock).mockResolvedValueOnce({
            data: { status: "unhealthy" },
        });

        render(<LoginPage />);

        const user = userEvent.setup();
        await user.type(screen.getByLabelText(/email/i), "test@example.com");
        await user.type(screen.getByLabelText(/password/i), "password123");

        await user.click(screen.getByRole("button", { name: "Sign In" }));

        await waitFor(() => {
            expect(apiClient.get).toHaveBeenCalledWith("/health");
            expect(screen.getByText("Backend is not healthy. Cannot login.")).toBeInTheDocument();
        });

        // Ensure router.push was not called
        expect(mockPush).not.toHaveBeenCalled();
    });

    it("shows error when connection fails (exception thrown)", async () => {
        // Mock network error
        (apiClient.get as jest.Mock).mockRejectedValueOnce(new Error("Network Error"));

        render(<LoginPage />);

        const user = userEvent.setup();
        await user.type(screen.getByLabelText(/email/i), "test@example.com");
        await user.type(screen.getByLabelText(/password/i), "password123");

        await user.click(screen.getByRole("button", { name: "Sign In" }));

        await waitFor(() => {
            expect(apiClient.get).toHaveBeenCalledWith("/health");
            expect(screen.getByText("Failed to connect to backend. Please ensure backend is running.")).toBeInTheDocument();
        });

        // Ensure router.push was not called
        expect(mockPush).not.toHaveBeenCalled();
    });
});

# Widle Insure Frontend

Next.js 14+ frontend for the AI-Automated Auto Insurance Claims Platform.

## Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn UI
- **Icons**: Lucide React

## Setup

1.  **Install Dependencies**:
    ```bash
    cd frontend
    npm install
    ```

2.  **Environment Variables**:
    Copy `.env.example` to `.env.local`:
    ```bash
    cp .env.example .env.local
    ```
    
3.  **Run Development Server**:
    ```bash
    npm run dev
    ```
    The app will be available at `http://localhost:3000`.

## Structure

*   `app/`: App Router pages and layouts
*   `components/ui/`: Shadcn UI components
*   `components/features/`: Feature-specific components
*   `lib/`: Utilities and API clients

## Week 1 Tasks
- [ ] Initialize Next.js project
- [ ] Setup Shadcn UI
- [ ] Connector to Backend Health Check
- [ ] Basic Insurance Theme

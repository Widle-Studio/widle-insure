import { ThemeToggle } from "@/components/theme-toggle";

export default function AppLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <div className="min-h-screen bg-slate-50 dark:bg-background">
            <nav className="border-b bg-white dark:bg-background px-4 py-3 shadow-material-1">
                <div className="container mx-auto flex flex-col md:flex-row items-center justify-between gap-4 md:gap-0">
                    <h1 className="text-xl font-bold text-slate-900 dark:text-slate-100">Widle Insure</h1>
                    <div className="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-4">
                        <a href="/dashboard" className="text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100">Dashboard</a>
                        <a href="/claims" className="text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100">Claims</a>
                        <a href="#" className="text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100">Settings</a>
                        <ThemeToggle />
                    </div>
                </div>
            </nav>
            <main className="container mx-auto py-8">
                {children}
            </main>
        </div>
    );
}

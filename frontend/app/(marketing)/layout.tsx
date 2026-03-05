import { ThemeToggle } from "@/components/theme-toggle";

export default function MarketingLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <div className="min-h-screen bg-background">
            <header className="fixed top-0 w-full z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
                <div className="container flex h-16 items-center justify-between">
                    <div className="flex gap-6 md:gap-10">
                        <a className="flex items-center space-x-2" href="/">
                            <span className="inline-block font-bold">Widle Insure</span>
                        </a>
                    </div>
                    <nav className="flex items-center gap-4">
                        <a href="/login" className="text-sm font-medium hover:underline underline-offset-4">Login</a>
                        <ThemeToggle />
                    </nav>
                </div>
            </header>
            <main className="flex-1 mt-16">
                {children}
            </main>
        </div>
    );
}

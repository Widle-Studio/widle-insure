import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "Widle Insure",
    description: "AI-Automated Auto Insurance Claims Platform",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={cn(inter.className, "min-h-screen bg-slate-50 antialiased")}>
                <nav className="border-b bg-white px-4 py-3 shadow-sm">
                    <div className="container mx-auto flex items-center justify-between">
                        <h1 className="text-xl font-bold text-slate-900">Widle Insure</h1>
                        <div className="space-x-4">
                            <a href="#" className="text-sm font-medium text-slate-600 hover:text-slate-900">Dashboard</a>
                            <a href="#" className="text-sm font-medium text-slate-600 hover:text-slate-900">Claims</a>
                            <a href="#" className="text-sm font-medium text-slate-600 hover:text-slate-900">Settings</a>
                        </div>
                    </div>
                </nav>
                <main className="container mx-auto py-8">
                    {children}
                </main>
            </body>
        </html>
    );
}

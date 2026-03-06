"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { apiClient } from "@/lib/api-client";

export default function Home() {
    const [health, setHealth] = useState<{ status: string; service?: string } | null>(null);

    useEffect(() => {
        apiClient.get("/health")
            .then(res => setHealth(res.data))
            .catch(err => setHealth({ status: "error" }));
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex flex-col space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">Welcome to Widle Insure</h1>
                <p className="text-slate-500">
                    AI-native automobile insurance claim settlement platform.
                </p>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card>
                    <CardHeader>
                        <CardTitle>System Status</CardTitle>
                        <CardDescription>Backend Connectivity</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center space-x-2">
                            <span className={`inline-block h-3 w-3 rounded-full ${health?.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'}`}></span>
                            <span className="font-medium">
                                {health ? (health.status === 'healthy' ? 'Operational' : 'Offline') : 'Checking...'}
                            </span>
                        </div>
                        {health?.service && <p className="mt-2 text-xs text-slate-400">{health.service}</p>}
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Quick Actions</CardTitle>
                        <CardDescription>Start managing claims</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-2">
                        <Button className="w-full">New Claim</Button>
                        <Button variant="outline" className="w-full">View Dashboard</Button>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

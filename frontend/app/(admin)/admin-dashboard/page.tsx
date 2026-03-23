"use client";

import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { apiClient } from "@/lib/api-client";

export default function AdminDashboardPage() {
    const [analytics, setAnalytics] = useState<{
        total_claims: number;
        approved_claims: number;
        pending_claims: number;
        rejected_claims: number;
        stp_rate: number;
    } | null>(null);

    useEffect(() => {
        // Assume API client handles auth token injection here via interceptors
        apiClient.get("/admin/claims/metrics/analytics")
            .then(res => setAnalytics(res.data))
            .catch(err => console.error(err));
    }, []);

    return (
        <div className="space-y-6 p-6">
            <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
            <p className="text-slate-500">Overview of claims platform metrics.</p>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader>
                        <CardTitle className="text-sm font-medium text-slate-500">Total Claims</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{analytics?.total_claims ?? 0}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle className="text-sm font-medium text-slate-500">Pending Review</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{analytics?.pending_claims ?? 0}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle className="text-sm font-medium text-slate-500">Approved</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{analytics?.approved_claims ?? 0}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle className="text-sm font-medium text-slate-500">STP Rate</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{analytics?.stp_rate ?? 0}%</div>
                    </CardContent>
                </Card>
            </div>
            {/* Charts could go here */}
        </div>
    );
}

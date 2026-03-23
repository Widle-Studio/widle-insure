"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/lib/api-client";

export default function AdminClaimsPage() {
    const [claims, setClaims] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        apiClient.get("/admin/claims")
            .then(res => setClaims(res.data))
            .catch(err => console.error(err))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="space-y-6 p-6">
            {loading && (
                <div className="space-y-4">
                    <div className="h-8 w-64 animate-pulse rounded-md bg-slate-200 dark:bg-slate-800" />
                    <div className="h-[400px] w-full animate-pulse rounded-md bg-slate-200 dark:bg-slate-800" />
                </div>
            )}
            {!loading && (
                <>
            <h1 className="text-3xl font-bold tracking-tight">Claims Management</h1>
            <Card>
                <CardHeader>
                    <CardTitle>Recent Claims</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="text-xs text-slate-500 bg-slate-50 uppercase">
                                <tr>
                                    <th className="px-6 py-3">Claim ID</th>
                                    <th className="px-6 py-3">Claimant</th>
                                    <th className="px-6 py-3">Status</th>
                                    <th className="px-6 py-3">Date</th>
                                    <th className="px-6 py-3">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {claims.map(claim => (
                                    <tr key={claim.id} className="border-b">
                                        <td className="px-6 py-4">{claim.claim_number}</td>
                                        <td className="px-6 py-4">{claim.claimant_name}</td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 rounded text-xs ${
                                                claim.status === 'Approved' ? 'bg-green-100 text-green-800' :
                                                claim.status === 'Rejected' ? 'bg-red-100 text-red-800' :
                                                'bg-yellow-100 text-yellow-800'
                                            }`}>
                                                {claim.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">{new Date(claim.created_at).toLocaleDateString()}</td>
                                        <td className="px-6 py-4">
                                            <Link href={`/claims/${claim.id}`}>
                                                <Button variant="outline" size="sm">View</Button>
                                            </Link>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>
            </>
            )}
        </div>
    );
}

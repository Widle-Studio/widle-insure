"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { apiClient } from "@/lib/api-client";
import Link from "next/link";

interface Claim {
    id: string;
    claim_number: string;
    status: string;
    fraud_score?: number | null;
    estimated_damage_cost?: number;
    claimant_name: string;
    created_at: string;
}

export default function ReviewQueuePage() {
    const [claims, setClaims] = useState<Claim[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        apiClient.get("/claims?status=Manual%20Review")
            .then(res => {
                setClaims(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch claims:", err);
                setLoading(false);
            });
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex flex-col space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">Review Queue</h1>
                <p className="text-slate-500">
                    Claims requiring human attention.
                </p>
            </div>

            <Card className="shadow-material-1">
                <CardHeader>
                    <CardTitle>Manual Review Required</CardTitle>
                    <CardDescription>Claims flagged for complex damage, fraud risk, or low AI confidence.</CardDescription>
                </CardHeader>
                <CardContent>
                    {loading ? (
                        <p>Loading claims...</p>
                    ) : claims.length === 0 ? (
                        <p className="text-slate-500">No claims currently require manual review.</p>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm text-left text-slate-500 dark:text-slate-400">
                                <thead className="text-xs text-slate-700 uppercase bg-slate-50 dark:bg-slate-700 dark:text-slate-400">
                                    <tr>
                                        <th scope="col" className="px-6 py-3">Claim Number</th>
                                        <th scope="col" className="px-6 py-3">Claimant</th>
                                        <th scope="col" className="px-6 py-3">Fraud Score</th>
                                        <th scope="col" className="px-6 py-3">Created At</th>
                                        <th scope="col" className="px-6 py-3">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {claims.map(claim => (
                                        <tr key={claim.id} className="bg-white border-b dark:bg-slate-800 dark:border-slate-700">
                                            <td className="px-6 py-4 font-medium text-slate-900 whitespace-nowrap dark:text-white">
                                                {claim.claim_number}
                                            </td>
                                            <td className="px-6 py-4">{claim.claimant_name}</td>
                                            <td className="px-6 py-4">
                                                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                                                    (claim.fraud_score || 0) > 30 ? 'bg-red-100 text-red-800' :
                                                    (claim.fraud_score || 0) > 10 ? 'bg-yellow-100 text-yellow-800' :
                                                    'bg-green-100 text-green-800'
                                                }`}>
                                                    {claim.fraud_score ?? "N/A"}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4">{new Date(claim.created_at).toLocaleDateString()}</td>
                                            <td className="px-6 py-4">
                                                <Link href={`/claims/${claim.id}`}>
                                                    <Button variant="outline" size="sm">Review</Button>
                                                </Link>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}

"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { apiClient } from "@/lib/api-client";
import { useParams } from "next/navigation";
import Link from "next/link";

export default function ClaimReviewPage() {
    const { id } = useParams();
    const [claim, setClaim] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!id) return;

        apiClient.get(`/claims/${id}`)
            .then(res => {
                setClaim(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch claim:", err);
                setError("Failed to load claim details.");
                setLoading(false);
            });
    }, [id]);

    if (loading) return <div>Loading claim...</div>;
    if (error || !claim) return <div>{error || "Claim not found"}</div>;

    const fraudScore = claim.fraud_score || 0;
    const fraudLevel = fraudScore > 30 ? "High" : fraudScore > 10 ? "Medium" : "Low";

    return (
        <div className="space-y-6">
            <div className="flex flex-col space-y-2">
                <div className="flex justify-between items-center">
                    <h1 className="text-3xl font-bold tracking-tight">Review Claim: {claim.claim_number}</h1>
                    <Link href="/claims">
                        <Button variant="outline">Back to Queue</Button>
                    </Link>
                </div>
                <p className="text-slate-500">
                    Review fraud indicators and adjudication details.
                </p>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card className="shadow-material-1 col-span-1 md:col-span-2 lg:col-span-2">
                    <CardHeader>
                        <CardTitle>Claim Details</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                        <p><strong>Claimant:</strong> {claim.claimant_name}</p>
                        <p><strong>Incident Date:</strong> {new Date(claim.incident_date || claim.created_at).toLocaleDateString()}</p>
                        <p><strong>Status:</strong> <span className="font-semibold">{claim.status}</span></p>
                        <p><strong>Adjudication Reason:</strong> {claim.adjudication_reason || "None"}</p>
                    </CardContent>
                </Card>

                <Card className="shadow-material-1">
                    <CardHeader>
                        <CardTitle>Fraud Indicators</CardTitle>
                        <CardDescription>System analysis of fraud risk</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex flex-col items-center p-4 border rounded-lg bg-slate-50 dark:bg-slate-800">
                            <span className="text-sm font-semibold mb-1">Fraud Score</span>
                            <span className={`text-4xl font-bold ${
                                fraudLevel === "High" ? 'text-red-600' :
                                fraudLevel === "Medium" ? 'text-yellow-600' :
                                'text-green-600'
                            }`}>
                                {fraudScore}
                            </span>
                            <span className="text-xs text-slate-500 uppercase mt-1">Risk: {fraudLevel}</span>
                        </div>

                        <div className="space-y-2 text-sm">
                            <p><strong>Specific Red Flags:</strong></p>
                            <ul className="list-disc pl-4 space-y-1">
                                {fraudScore > 0 ? (
                                    <>
                                        {(fraudScore >= 20) && <li>Potential delay in reporting incident</li>}
                                        {fraudLevel === "High" && <li>Multiple factors indicate increased risk</li>}
                                    </>
                                ) : (
                                    <li className="text-slate-500">No red flags detected.</li>
                                )}
                            </ul>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <div className="flex space-x-4">
                <Button className="bg-green-600 hover:bg-green-700 text-white">Approve Claim</Button>
                <Button variant="destructive">Reject Claim</Button>
                <Button variant="outline">Request Info</Button>
            </div>
        </div>
    );
}
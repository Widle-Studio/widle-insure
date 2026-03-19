"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { apiClient } from "@/lib/api-client";
import { Loader2 } from "lucide-react";

export default function ClaimStatusPage() {
    const [claimNumber, setClaimNumber] = useState("");
    const [claim, setClaim] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleLookup = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setClaim(null);

        try {
            const res = await apiClient.get(`/claims/lookup/${claimNumber}`);
            setClaim(res.data);
        } catch (err: any) {
            console.error(err);
            setError("Claim not found or an error occurred.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col min-h-[70vh] items-center justify-center p-4">
            <Card className="w-full max-w-md shadow-lg">
                <CardHeader>
                    <CardTitle className="text-2xl font-bold text-center">Check Claim Status</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleLookup} className="space-y-4">
                        <div className="space-y-2">
                            <label htmlFor="claimNumber" className="text-sm font-medium">Claim Number</label>
                            <Input
                                id="claimNumber"
                                placeholder="e.g. CLM-2025-123456"
                                value={claimNumber}
                                onChange={(e) => setClaimNumber(e.target.value)}
                                required
                            />
                        </div>
                        <Button type="submit" className="w-full" disabled={loading}>
                            {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : "Lookup Status"}
                        </Button>
                    </form>

                    {error && (
                        <div className="mt-4 p-3 bg-red-50 text-red-600 rounded text-sm text-center">
                            {error}
                        </div>
                    )}

                    {claim && (
                        <div className="mt-6 space-y-4 border-t pt-4">
                            <div className="flex justify-between items-center">
                                <span className="font-medium text-slate-500">Status</span>
                                <span className={`px-2 py-1 rounded text-xs font-semibold ${
                                    claim.status === 'Approved' ? 'bg-green-100 text-green-800' :
                                    claim.status === 'Rejected' ? 'bg-red-100 text-red-800' :
                                    claim.status === 'Paid' ? 'bg-blue-100 text-blue-800' :
                                    'bg-yellow-100 text-yellow-800'
                                }`}>
                                    {claim.status}
                                </span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="font-medium text-slate-500">Date Filed</span>
                                <span>{new Date(claim.created_at).toLocaleDateString()}</span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="font-medium text-slate-500">Vehicle</span>
                                <span>{claim.vehicle_year} {claim.vehicle_make} {claim.vehicle_model}</span>
                            </div>

                            {(claim.status === "Approved" || claim.status === "Paid") && claim.approved_amount && (
                                <div className="flex justify-between items-center mt-4 p-3 bg-slate-50 rounded border">
                                    <span className="font-bold">Approved Amount</span>
                                    <span className="font-bold text-lg text-primary">${parseFloat(claim.approved_amount).toLocaleString()}</span>
                                </div>
                            )}
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}

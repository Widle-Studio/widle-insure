"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/lib/api-client";

export default function ClaimDetailPage() {
    const params = useParams();
    const router = useRouter();
    const [claim, setClaim] = useState<any>(null);

    useEffect(() => {
        if (params.id) {
            apiClient.get(`/admin/claims/${params.id}`)
                .then(res => setClaim(res.data))
                .catch(err => console.error(err));
        }
    }, [params.id]);

    const handleAction = async (action: 'approve' | 'reject' | 'payout') => {
        // User Experience: Add Confirmation Dialogs for destructive/important actions
        const confirmMsg = action === 'reject'
            ? "Are you sure you want to REJECT this claim? This action cannot be easily undone."
            : action === 'approve'
            ? "Are you sure you want to APPROVE this claim?"
            : "Are you sure you want to initiate payout?";

        if (!window.confirm(confirmMsg)) return;

        try {
            if (action === 'payout') {
                const res = await apiClient.post(`/payments/${params.id}/payout`);
                setClaim(res.data);
                alert(`Claim payout initiated successfully`);
            } else {
                const res = await apiClient.post(`/admin/claims/${params.id}/${action}`);
                setClaim(res.data);
                alert(`Claim successfully ${action}ed`);
            }
            router.refresh();
        } catch (error) {
            console.error(error);
            alert(`Failed to ${action} claim`);
        }
    };

    if (!claim) return <div className="p-6">Loading...</div>;

    return (
        <div className="space-y-6 p-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <h1 className="text-3xl font-bold tracking-tight">Claim: {claim.claim_number}</h1>
                <div className="flex flex-wrap gap-2">
                    {claim.status === "Approved" && (
                        <Button onClick={() => handleAction('payout')} className="bg-blue-600 hover:bg-blue-700 text-white">Initiate Payout</Button>
                    )}
                    {claim.status !== "Approved" && claim.status !== "Rejected" && claim.status !== "Paid" && (
                        <>
                            <Button onClick={() => handleAction('approve')} className="bg-green-600 hover:bg-green-700 text-white">Approve</Button>
                            <Button onClick={() => handleAction('reject')} variant="destructive">Reject</Button>
                        </>
                    )}
                </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle>Claimant Information</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                        <p><strong>Name:</strong> {claim.claimant_name}</p>
                        <p><strong>Email:</strong> {claim.claimant_email}</p>
                        <p><strong>Phone:</strong> {claim.claimant_phone}</p>
                        <p><strong>Policy Number:</strong> {claim.policy_number}</p>
                        <p><strong>Status:</strong> {claim.status}</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Incident Details</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                        <p><strong>Date:</strong> {new Date(claim.incident_date).toLocaleString()}</p>
                        <p><strong>Location:</strong> {claim.incident_location}</p>
                        <p><strong>Description:</strong> {claim.incident_description}</p>
                    </CardContent>
                </Card>

                <Card className="md:col-span-2">
                    <CardHeader>
                        <CardTitle>Vehicle Information</CardTitle>
                    </CardHeader>
                    <CardContent className="grid grid-cols-2 gap-4">
                        <p><strong>Make:</strong> {claim.vehicle_make}</p>
                        <p><strong>Model:</strong> {claim.vehicle_model}</p>
                        <p><strong>Year:</strong> {claim.vehicle_year}</p>
                        <p><strong>VIN:</strong> {claim.vehicle_vin}</p>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

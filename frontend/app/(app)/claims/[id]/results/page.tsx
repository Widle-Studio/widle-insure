"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { apiClient } from "@/lib/api-client";
import { Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function ClaimResultsPage() {
    const params = useParams();
    const [claim, setClaim] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (params.id) {
            const fetchClaim = async () => {
                try {
                    const res = await apiClient.get(`/api/v1/claims/${params.id}`);
                    setClaim(res.data);
                } catch (err) {
                    console.error(err);
                } finally {
                    setLoading(false);
                }
            };
            fetchClaim();
        }
    }, [params.id]);

    if (loading || !claim) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[50vh] space-y-4">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                <h2 className="text-xl font-semibold">AI is analyzing your claim...</h2>
                <p className="text-muted-foreground text-center max-w-md">
                    Our advanced computer vision models are evaluating the damage to estimate repair costs.
                </p>
            </div>
        );
    }

    const analysis = claim.photos?.[0]?.ai_analysis;

    return (
        <div className="max-w-4xl mx-auto p-4 space-y-6">
            <div className="flex flex-col space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">Damage Assessment Results</h1>
                <p className="text-muted-foreground">Claim #{claim.claim_number}</p>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                <Card className="shadow-lg border-primary/20">
                    <CardHeader className="bg-primary/5 border-b pb-4">
                        <CardTitle className="text-xl">Estimated Cost</CardTitle>
                    </CardHeader>
                    <CardContent className="pt-6">
                        <div className="text-4xl font-bold text-primary">
                            ${claim.estimated_damage_cost?.toLocaleString() || "Pending"}
                        </div>
                        {analysis && (
                            <div className="mt-4 space-y-2">
                                <div className="flex justify-between border-b pb-2">
                                    <span className="text-muted-foreground">Severity:</span>
                                    <span className="font-medium capitalize">{analysis.severity}</span>
                                </div>
                                <div className="flex justify-between border-b pb-2">
                                    <span className="text-muted-foreground">Confidence:</span>
                                    <span className="font-medium">{(analysis.confidence * 100).toFixed(0)}%</span>
                                </div>
                            </div>
                        )}
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="text-xl">Analysis Reasoning</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-slate-700 leading-relaxed">
                            {analysis?.reasoning || "Analysis is still pending or not available."}
                        </p>
                        {analysis?.damaged_parts?.length > 0 && (
                            <div className="mt-4">
                                <h4 className="font-semibold mb-2">Identified Damaged Parts:</h4>
                                <ul className="list-disc pl-5 space-y-1">
                                    {analysis.damaged_parts.map((part: string, idx: number) => (
                                        <li key={idx} className="capitalize">{part.replace("_", " ")}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>

            {claim.photos?.length > 0 && (
                <div className="space-y-4">
                    <h3 className="text-xl font-semibold">Analyzed Photos</h3>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        {claim.photos.map((photo: any) => (
                            <div key={photo.id} className="relative aspect-video rounded-lg overflow-hidden border shadow-sm">
                                <img src={`http://localhost:8000${photo.photo_url}`} alt="Damage" className="object-cover w-full h-full" />
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <div className="flex justify-end pt-6 border-t">
                <Link href="/dashboard">
                    <Button>Return to Dashboard</Button>
                </Link>
            </div>
        </div>
    );
}

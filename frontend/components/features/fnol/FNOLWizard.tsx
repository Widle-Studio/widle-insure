"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod"; // We will add Zod schema later
import { Button } from "@/components/ui/button";
import { Step1Policy } from "./Step1Policy";
import { Step2Incident } from "./Step2Incident";
import { Step3Vehicle } from "./Step3Vehicle";
import { PhotoUpload } from "./PhotoUpload";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { apiClient } from "@/lib/api-client";
import { Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";

import { FNOLFormData } from "@/types/fnol";

import { motion, AnimatePresence } from "framer-motion";

// Field groups for validation per step
const STEP_FIELDS: Record<number, (keyof FNOLFormData)[]> = {
    1: ["policy_number", "claimant_name", "claimant_email", "claimant_phone"],
    2: ["incident_date", "incident_location", "incident_description"],
    3: ["vehicle_year", "vehicle_make", "vehicle_model", "vehicle_vin"],
};

export function FNOLWizard() {
    const [step, setStep] = useState(1);
    const [photos, setPhotos] = useState<File[]>([]);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const router = useRouter();
    const totalSteps = 4;

    // ... (rest of form setup)

    const form = useForm<FNOLFormData>({
        mode: "onChange", // Validate on change for better UX in wizard
        // resolver: zodResolver(schema) // Add schema later
    });

    const { handleSubmit, trigger, formState: { isValid } } = form;

    const nextStep = async () => {
        const fields = STEP_FIELDS[step];
        const isStepValid = await trigger(fields); // Trigger validation for current step fields only

        if (isStepValid) {
            setStep((prev) => prev + 1);
        }
    };

    const prevStep = () => {
        setStep((prev) => prev - 1);
    };

    const onPhotosSelected = (files: File[]) => {
        setPhotos(files);
    };

    const onSubmit = async (data: FNOLFormData) => {
        setIsSubmitting(true);
        try {
            // 1. Create Claim
            const claimResponse = await apiClient.post("/api/v1/claims", data);
            const claimId = claimResponse.data.id;

            // 2. Upload Photos
            if (photos.length > 0) {
                // Upload concurrently
                await Promise.all(photos.map(photo => {
                    const formData = new FormData();
                    formData.append("file", photo);
                    return apiClient.post(`/api/v1/claims/${claimId}/photos`, formData, {
                        headers: { "Content-Type": "multipart/form-data" }
                    });
                }));
            }

            // 3. Redirect to Success/Summary Page
            router.push(`/?claim_id=${claimId}&status=submitted`); // Temporary redirect to home
        } catch (error) {
            console.error("Error submitting claim:", error);
            alert("Failed to submit claim. Please try again.");
        } finally {
            setIsSubmitting(false);
        }
    };

    const progress = (step / totalSteps) * 100;

    return (
        <div className="max-w-2xl mx-auto p-4 space-y-6">
            <div className="flex flex-col space-y-2">
                <div className="flex justify-between items-center">
                    <h2 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
                        File a New Claim
                    </h2>
                    <span className="text-sm font-medium text-muted-foreground">Step {step} of {totalSteps}</span>
                </div>
                {/* Modern Progress Bar */}
                <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                    <motion.div
                        className="h-full bg-primary"
                        initial={{ width: 0 }}
                        animate={{ width: `${progress}%` }}
                        transition={{ duration: 0.5, ease: "easeInOut" }}
                    />
                </div>
            </div>

            <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
                <CardHeader>
                    {/* Header content moved to step components if needed, or kept generic */}
                </CardHeader>
                <CardContent className="p-6">
                    <form onSubmit={handleSubmit(onSubmit)}>
                        <div className="min-h-[400px]">
                            <AnimatePresence mode="wait">
                                <motion.div
                                    key={step}
                                    initial={{ x: 20, opacity: 0 }}
                                    animate={{ x: 0, opacity: 1 }}
                                    exit={{ x: -20, opacity: 0 }}
                                    transition={{ duration: 0.3 }}
                                >
                                    {step === 1 && <Step1Policy form={form} />}
                                    {step === 2 && <Step2Incident form={form} />}
                                    {step === 3 && <Step3Vehicle form={form} />}
                                    {step === 4 && <PhotoUpload onPhotosSelected={onPhotosSelected} />}
                                </motion.div>
                            </AnimatePresence>
                        </div>

                        <div className="mt-8 flex justify-between pt-4 border-t">
                            <Button
                                type="button"
                                variant="outline"
                                onClick={prevStep}
                                disabled={step === 1 || isSubmitting}
                                className="w-32"
                            >
                                Back
                            </Button>

                            {step < totalSteps ? (
                                <Button type="button" onClick={nextStep} className="w-32">
                                    Next
                                </Button>
                            ) : (
                                <Button type="submit" disabled={isSubmitting} className="w-40 bg-gradient-to-r from-primary to-blue-600 hover:opacity-90 transition-opacity">
                                    {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                    Submit Claim
                                </Button>
                            )}
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}

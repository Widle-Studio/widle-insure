import { UseFormReturn } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { FNOLFormData } from "@/types/fnol";

interface Step2Props {
    form: UseFormReturn<FNOLFormData>;
}

export function Step2Incident({ form }: Step2Props) {
    const { register, formState: { errors } } = form;

    return (
        <Card>
            <CardHeader>
                <CardTitle>Incident Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="space-y-2">
                    <Label htmlFor="incident_date">Date & Time</Label>
                    <Input
                        id="incident_date"
                        type="datetime-local"
                        {...register("incident_date", { required: "Date is required" })}
                    />
                    {errors.incident_date && (
                        <p className="text-sm text-red-500">{String(errors.incident_date.message)}</p>
                    )}
                </div>

                <div className="space-y-2">
                    <Label htmlFor="incident_location">Location</Label>
                    <Input
                        id="incident_location"
                        placeholder="123 Main St, Springfield"
                        {...register("incident_location", { required: "Location is required" })}
                    />
                    {errors.incident_location && (
                        <p className="text-sm text-red-500">{String(errors.incident_location.message)}</p>
                    )}
                </div>

                <div className="space-y-2">
                    <Label htmlFor="incident_description">Description</Label>
                    <Textarea
                        id="incident_description"
                        placeholder="Describe what happened..."
                        {...register("incident_description", { required: "Description is required" })}
                    />
                    {errors.incident_description && (
                        <p className="text-sm text-red-500">{String(errors.incident_description.message)}</p>
                    )}
                </div>
            </CardContent>
        </Card>
    );
}

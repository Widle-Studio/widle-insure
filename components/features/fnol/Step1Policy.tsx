import { UseFormReturn } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { FNOLFormData } from "@/types/fnol";

interface Step1Props {
    form: UseFormReturn<FNOLFormData>;
}

export function Step1Policy({ form }: Step1Props) {
    const { register, formState: { errors } } = form;

    return (
        <Card>
            <CardHeader>
                <CardTitle>Claimant & Policy Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="space-y-2">
                    <Label htmlFor="policy_number">Policy Number</Label>
                    <Input
                        id="policy_number"
                        placeholder="POL-XXXXXXXX"
                        {...register("policy_number", { required: "Policy number is required" })}
                    />
                    {errors.policy_number && (
                        <p className="text-sm text-red-500">{String(errors.policy_number.message)}</p>
                    )}
                </div>

                <div className="space-y-2">
                    <Label htmlFor="claimant_name">Full Name</Label>
                    <Input
                        id="claimant_name"
                        placeholder="John Doe"
                        {...register("claimant_name", { required: "Name is required" })}
                    />
                    {errors.claimant_name && (
                        <p className="text-sm text-red-500">{String(errors.claimant_name.message)}</p>
                    )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label htmlFor="claimant_email">Email</Label>
                        <Input
                            id="claimant_email"
                            type="email"
                            placeholder="john@example.com"
                            {...register("claimant_email", { required: "Email is required" })}
                        />
                        {errors.claimant_email && (
                            <p className="text-sm text-red-500">{String(errors.claimant_email.message)}</p>
                        )}
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="claimant_phone">Phone</Label>
                        <Input
                            id="claimant_phone"
                            placeholder="555-0123"
                            {...register("claimant_phone", { required: "Phone is required" })}
                        />
                        {errors.claimant_phone && (
                            <p className="text-sm text-red-500">{String(errors.claimant_phone.message)}</p>
                        )}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}

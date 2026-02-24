import { UseFormReturn } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { FNOLFormData } from "@/types/fnol";

interface Step3Props {
    form: UseFormReturn<FNOLFormData>;
}

export function Step3Vehicle({ form }: Step3Props) {
    const { register, formState: { errors } } = form;

    return (
        <Card>
            <CardHeader>
                <CardTitle>Vehicle Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="space-y-2">
                    <Label htmlFor="vehicle_year">Year</Label>
                    <Input
                        id="vehicle_year"
                        type="number"
                        placeholder="2022"
                        {...register("vehicle_year", { required: "Year is required", valueAsNumber: true })}
                    />
                    {errors.vehicle_year && (
                        <p className="text-sm text-red-500">{String(errors.vehicle_year.message)}</p>
                    )}
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label htmlFor="vehicle_make">Make</Label>
                        <Input
                            id="vehicle_make"
                            placeholder="Toyota"
                            {...register("vehicle_make", { required: "Make is required" })}
                        />
                        {errors.vehicle_make && (
                            <p className="text-sm text-red-500">{String(errors.vehicle_make.message)}</p>
                        )}
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="vehicle_model">Model</Label>
                        <Input
                            id="vehicle_model"
                            placeholder="Camry"
                            {...register("vehicle_model", { required: "Model is required" })}
                        />
                        {errors.vehicle_model && (
                            <p className="text-sm text-red-500">{String(errors.vehicle_model.message)}</p>
                        )}
                    </div>
                </div>

                <div className="space-y-2">
                    <Label htmlFor="vehicle_vin">VIN (Optional)</Label>
                    <Input
                        id="vehicle_vin"
                        placeholder="XXXXXXXXXXXXXXXXX"
                        {...register("vehicle_vin")}
                    />
                </div>
            </CardContent>
        </Card>
    );
}

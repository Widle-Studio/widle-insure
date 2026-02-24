export interface FNOLFormData {
    policy_number: string;
    claimant_name: string;
    claimant_email: string;
    claimant_phone: string;
    incident_date: string;
    incident_location: string;
    incident_description: string;
    vehicle_year: number;
    vehicle_make: string;
    vehicle_model: string;
    vehicle_vin?: string;
}

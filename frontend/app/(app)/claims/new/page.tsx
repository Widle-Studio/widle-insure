"use client";

import { FNOLWizard } from "@/components/features/fnol/FNOLWizard";

export default function NewClaimPage() {
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6 text-center">File a New Claim</h1>
      <p className="text-center text-gray-500 mb-8 max-w-2xl mx-auto">
        We're sorry you experienced an incident. Please provide the details below, and our AI-powered system will process your claim immediately.
      </p>
      <FNOLWizard />
    </div>
  );
}

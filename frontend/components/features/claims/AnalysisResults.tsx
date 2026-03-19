"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, AlertTriangle } from "lucide-react";

interface AnalysisResultsProps {
  analysis: {
    severity: "minor" | "moderate" | "major" | "total_loss";
    damaged_parts: string[];
    estimated_cost: number;
    confidence: number;
    fraud_indicators: string[];
    reasoning: string;
  };
}

export function AnalysisResults({ analysis }: AnalysisResultsProps) {
  const severityColor = {
    minor: "bg-green-500",
    moderate: "bg-yellow-500",
    major: "bg-orange-500",
    total_loss: "bg-red-500",
  }[analysis.severity];

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>AI Damage Assessment</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Severity */}
          <div className="flex items-center justify-between">
            <span className="font-medium">Severity</span>
            <Badge className={severityColor}>
              {analysis.severity.replace("_", " ").toUpperCase()}
            </Badge>
          </div>

          {/* Estimated Cost */}
          <div className="flex items-center justify-between">
            <span className="font-medium">Estimated Repair Cost</span>
            <span className="text-2xl font-bold">
              ${analysis.estimated_cost.toLocaleString()}
            </span>
          </div>

          {/* Confidence */}
          <div className="flex items-center justify-between">
            <span className="font-medium">AI Confidence</span>
            <div className="flex items-center gap-2">
              <div className="w-32 h-2 bg-gray-200 rounded">
                <div
                  className="h-2 bg-primary rounded"
                  style={{ width: `${analysis.confidence * 100}%` }}
                />
              </div>
              <span className="text-sm">
                {(analysis.confidence * 100).toFixed(0)}%
              </span>
            </div>
          </div>

          {/* Damaged Parts */}
          <div>
            <p className="font-medium mb-2">Damaged Parts</p>
            <div className="flex flex-wrap gap-2">
              {analysis.damaged_parts.map((part) => (
                <Badge key={part} variant="outline">
                  {part.replace("_", " ")}
                </Badge>
              ))}
            </div>
          </div>

          {/* Fraud Indicators */}
          {analysis.fraud_indicators.length > 0 && (
            <div className="bg-red-50 p-4 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <AlertTriangle className="h-5 w-5 text-red-500" />
                <span className="font-medium text-red-900">
                  Fraud Indicators Detected
                </span>
              </div>
              <ul className="list-disc list-inside text-sm text-red-800">
                {analysis.fraud_indicators.map((indicator, i) => (
                  <li key={i}>{indicator}</li>
                ))}
              </ul>
            </div>
          )}

          {/* AI Reasoning */}
          <div>
            <p className="font-medium mb-2">Analysis Details</p>
            <p className="text-sm text-muted-foreground">
              {analysis.reasoning}
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

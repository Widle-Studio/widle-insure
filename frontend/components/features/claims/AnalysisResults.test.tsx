import { render, screen } from '@testing-library/react';
import { AnalysisResults } from './AnalysisResults';
import '@testing-library/jest-dom';

describe('AnalysisResults', () => {
  const mockAnalysis = {
    severity: 'moderate' as const,
    damaged_parts: ['front_bumper', 'hood'],
    estimated_cost: 2500,
    confidence: 0.85,
    fraud_indicators: ['Mismatched damage pattern'],
    reasoning: 'Mock reasoning text',
    fraud_score: 45
  };

  it('renders analysis details correctly', () => {
    render(<AnalysisResults analysis={mockAnalysis} />);

    // Check severity
    expect(screen.getByText('MODERATE')).toBeInTheDocument();

    // Check cost
    expect(screen.getByText('$2,500')).toBeInTheDocument();

    // Check damaged parts
    expect(screen.getByText('front bumper')).toBeInTheDocument();
    expect(screen.getByText('hood')).toBeInTheDocument();

    // Check fraud score
    expect(screen.getByText('Fraud Risk Score')).toBeInTheDocument();
    expect(screen.getByText('45 / 100')).toBeInTheDocument();

    // Check fraud indicators
    expect(screen.getByText('Fraud Indicators Detected')).toBeInTheDocument();
    expect(screen.getByText('Mismatched damage pattern')).toBeInTheDocument();

    // Check reasoning
    expect(screen.getByText('Mock reasoning text')).toBeInTheDocument();
  });
});

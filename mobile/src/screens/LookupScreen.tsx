import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, SafeAreaView, StyleSheet, ActivityIndicator } from 'react-native';
import { apiClient } from '../api/client';

export default function LookupScreen() {
  const [claimNumber, setClaimNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [claimData, setClaimData] = useState<any>(null);
  const [error, setError] = useState('');

  const handleLookup = async () => {
    if (!claimNumber.trim()) {
      setError('Please enter a claim number');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await apiClient.get(`/claims/lookup/${claimNumber}`);
      setClaimData(response.data);
    } catch (err: any) {
      console.log(err);
      setError('Claim not found or API error.');
      setClaimData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Track Claim</Text>

        <TextInput
          style={styles.input}
          placeholder="Enter Claim Number (e.g., CLM-2025-...)"
          value={claimNumber}
          onChangeText={setClaimNumber}
          autoCapitalize="none"
        />

        <TouchableOpacity
          style={styles.button}
          onPress={handleLookup}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Search</Text>
          )}
        </TouchableOpacity>

        {error ? <Text style={styles.error}>{error}</Text> : null}

        {claimData && (
          <View style={styles.resultCard}>
            <Text style={styles.resultTitle}>Claim Details</Text>
            <Text style={styles.resultLabel}>Status: <Text style={styles.resultValue}>{claimData.status}</Text></Text>
            <Text style={styles.resultLabel}>Vehicle: <Text style={styles.resultValue}>{claimData.vehicle_year} {claimData.vehicle_make} {claimData.vehicle_model}</Text></Text>
            {claimData.approved_amount && (
              <Text style={styles.resultLabel}>Approved Amount: <Text style={styles.resultValue}>${claimData.approved_amount}</Text></Text>
            )}
          </View>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    padding: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 24,
    color: '#1f2937',
  },
  input: {
    borderWidth: 1,
    borderColor: '#d1d5db',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    marginBottom: 16,
  },
  button: {
    backgroundColor: '#3b82f6',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  error: {
    color: '#ef4444',
    marginTop: 16,
    textAlign: 'center',
  },
  resultCard: {
    marginTop: 32,
    padding: 16,
    backgroundColor: '#f3f4f6',
    borderRadius: 8,
  },
  resultTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#1f2937',
  },
  resultLabel: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 8,
  },
  resultValue: {
    fontWeight: '600',
    color: '#1f2937',
  },
});

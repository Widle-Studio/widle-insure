import React, { useState } from 'react';
import { View, Text, TouchableOpacity, SafeAreaView, StyleSheet, Image, ScrollView, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

export default function FNOLScreen() {
  const [images, setImages] = useState<string[]>([]);

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsEditing: true,
      quality: 1,
    });

    if (!result.canceled) {
      setImages([...images, result.assets[0].uri]);
    }
  };

  const takePhoto = async () => {
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();

    if (permissionResult.granted === false) {
      Alert.alert("Permission Required", "You need to grant camera permission to use this feature.");
      return;
    }

    let result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      quality: 1,
    });

    if (!result.canceled) {
      setImages([...images, result.assets[0].uri]);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>New Claim Submission</Text>
        <Text style={styles.subtitle}>Step 1: Capture Damage Photos</Text>

        <View style={styles.buttonRow}>
          <TouchableOpacity style={styles.buttonSecondary} onPress={takePhoto}>
            <Text style={styles.buttonTextSecondary}>Take Photo</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.buttonSecondary} onPress={pickImage}>
            <Text style={styles.buttonTextSecondary}>Upload from Gallery</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.imageGrid}>
          {images.map((uri, index) => (
            <Image key={index} source={{ uri }} style={styles.image} />
          ))}
        </View>

        {images.length > 0 && (
          <TouchableOpacity style={styles.buttonPrimary}>
            <Text style={styles.buttonTextPrimary}>Continue to Details</Text>
          </TouchableOpacity>
        )}
      </ScrollView>
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
    color: '#1f2937',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#6b7280',
    marginBottom: 24,
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 24,
  },
  buttonSecondary: {
    backgroundColor: '#f3f4f6',
    padding: 12,
    borderRadius: 8,
    flex: 0.48,
    alignItems: 'center',
  },
  buttonTextSecondary: {
    color: '#374151',
    fontWeight: '600',
  },
  imageGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 32,
  },
  image: {
    width: '31%',
    aspectRatio: 1,
    borderRadius: 8,
  },
  buttonPrimary: {
    backgroundColor: '#3b82f6',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonTextPrimary: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

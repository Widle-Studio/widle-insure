import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from '../screens/HomeScreen';
import LookupScreen from '../screens/LookupScreen';
import FNOLScreen from '../screens/FNOLScreen';
import { RootStackParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: 'Widle Insure' }}
        />
        <Stack.Screen
          name="Lookup"
          component={LookupScreen}
          options={{ title: 'Claim Status' }}
        />
        <Stack.Screen
          name="FNOL"
          component={FNOLScreen}
          options={{ title: 'New Claim' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

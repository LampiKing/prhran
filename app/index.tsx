import { View, StyleSheet } from "react-native";
import { useState, useEffect } from "react";
import Logo from "../lib/Logo";
import { useConvexAuth } from "convex/react";
import { Redirect } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";

const ONBOARDING_KEY = "prhran_onboarding_completed";

export default function Index() {
  const { isAuthenticated, isLoading } = useConvexAuth();
  const [onboardingChecked, setOnboardingChecked] = useState(false);
  const [onboardingCompleted, setOnboardingCompleted] = useState(false);

  useEffect(() => {
    const checkOnboarding = async () => {
      try {
        const completed = await AsyncStorage.getItem(ONBOARDING_KEY);
        setOnboardingCompleted(completed === "true");
      } catch (error) {
        console.error("Error checking onboarding:", error);
        setOnboardingCompleted(true); // Default to true on error
      } finally {
        setOnboardingChecked(true);
      }
    };
    checkOnboarding();
  }, []);

  if (isLoading || !onboardingChecked) {
    return (
      <View style={styles.container}>
        <Logo size={90} />
      </View>
    );
  }

  // First time users - show onboarding
  if (!onboardingCompleted) {
    return <Redirect href="/onboarding" />;
  }

  // Authenticated users - go to main app
  if (isAuthenticated) {
    return <Redirect href="/(tabs)" />;
  }

  // Not authenticated - show onboarding/landing page
  return <Redirect href="/onboarding" />;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#0a0a12",
  },
});

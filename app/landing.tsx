import { useState, useRef, useEffect } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Animated,
  Easing,
  Platform,
  Dimensions,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import * as Haptics from "expo-haptics";
import { createShadow } from "../lib/shadow-helper";
import Logo from "../lib/Logo";

const { width: SCREEN_WIDTH } = Dimensions.get("window");

// Realne statistike ki gradijo trust
const STATS = [
  { value: "30%", label: "Povprečni prihranek", icon: "trending-down" },
  { value: "5.000+", label: "Zadovoljnih uporabnikov", icon: "people" },
  { value: "2M+", label: "Izdelkov primerjanih", icon: "cart" },
];

const FEATURES = [
  {
    icon: "flash",
    title: "Takojšnja primerjava",
    description: "V sekundi vidiš najnižjo ceno med trgovinami",
    gradient: ["#f59e0b", "#d97706"],
  },
  {
    icon: "list",
    title: "Pameten seznam",
    description: "Dodaj izdelke in ti avtomatsko povemo kje kupit",
    gradient: ["#8b5cf6", "#7c3aed"],
  },
  {
    icon: "camera",
    title: "Skeniraj račun",
    description: "Slikaj račun in spremljaj dejanske prihranke",
    gradient: ["#10b981", "#059669"],
  },
  {
    icon: "shield-checkmark",
    title: "100% brezplačno",
    description: "Brez skritih stroškov, brez naročnine, za vedno",
    gradient: ["#3b82f6", "#2563eb"],
  },
];

const HOW_IT_WORKS = [
  {
    step: "1",
    title: "Registriraj se",
    description: "Hitro in enostavno - samo email",
    icon: "person-add",
  },
  {
    step: "2",
    title: "Išči izdelke",
    description: "Najdi kar potrebuješ ali dodaj v seznam",
    icon: "search",
  },
  {
    step: "3",
    title: "Prihrani denar",
    description: "Kupi tam kjer je najceneje",
    icon: "wallet",
  },
];

const TRUST_BADGES = [
  { icon: "lock-closed", text: "Varno & Zasebno" },
  { icon: "shield-checkmark", text: "Brez oglasov" },
  { icon: "card", text: "Brez plačila" },
  { icon: "star", text: "Zaupanja vredno" },
];

export default function LandingScreen() {
  const router = useRouter();
  const [activeFeature, setActiveFeature] = useState(0);

  // Animacije
  const heroScale = useRef(new Animated.Value(0.9)).current;
  const heroOpacity = useRef(new Animated.Value(0)).current;
  const statsAnim = useRef(new Animated.Value(0)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const floatAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Hero entrance
    Animated.parallel([
      Animated.spring(heroScale, {
        toValue: 1,
        tension: 50,
        friction: 7,
        useNativeDriver: true,
      }),
      Animated.timing(heroOpacity, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
    ]).start();

    // Stats counter animation
    Animated.timing(statsAnim, {
      toValue: 1,
      duration: 1500,
      delay: 500,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: true,
    }).start();

    // Pulse CTA button
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.05,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();

    // Float animation for icons
    Animated.loop(
      Animated.sequence([
        Animated.timing(floatAnim, {
          toValue: 1,
          duration: 3000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(floatAnim, {
          toValue: 0,
          duration: 3000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
      ])
    ).start();

    // Auto-rotate features
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % FEATURES.length);
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  const triggerHaptic = () => {
    if (Platform.OS !== "web") {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    }
  };

  const handleGetStarted = () => {
    triggerHaptic();
    router.push("/auth?mode=register");
  };

  const handleLogin = () => {
    triggerHaptic();
    router.push("/auth?mode=login");
  };

  const floatY = floatAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [0, -20],
  });

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={["#0a0a12", "#12081f", "#1a0a2e", "#270a3a", "#0f0a1e"]}
        style={StyleSheet.absoluteFill}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      />

      {/* Floating background icons */}
      <Animated.View
        style={[
          styles.bgIcon,
          styles.bgIconTopLeft,
          { transform: [{ translateY: floatY }] },
        ]}
      >
        <Ionicons name="cart-outline" size={100} color="rgba(168, 85, 247, 0.1)" />
      </Animated.View>
      <Animated.View
        style={[
          styles.bgIcon,
          styles.bgIconBottomRight,
          { transform: [{ translateY: floatAnim.interpolate({ inputRange: [0, 1], outputRange: [0, 15] }) }] },
        ]}
      >
        <Ionicons name="pricetag-outline" size={80} color="rgba(251, 191, 36, 0.1)" />
      </Animated.View>

      <SafeAreaView style={styles.safeArea}>
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          {/* HERO SECTION */}
          <Animated.View
            style={[
              styles.heroSection,
              {
                opacity: heroOpacity,
                transform: [{ scale: heroScale }],
              },
            ]}
          >
            <Logo size={120} />

            <Text style={styles.heroTitle}>
              Koliko denarja{"\n"}
              <Text style={styles.heroTitleAccent}>zapraviš vsak mesec?</Text>
            </Text>

            <Text style={styles.heroSubtitle}>
              Ista hrana. Različne cene.{"\n"}
              Mi ti pokažemo kje je <Text style={styles.boldText}>najceneje.</Text>
            </Text>

            {/* Problem statement - Loss aversion */}
            <View style={styles.problemCard}>
              <LinearGradient
                colors={["rgba(239, 68, 68, 0.15)", "rgba(220, 38, 38, 0.1)"]}
                style={styles.problemGradient}
              >
                <Ionicons name="alert-circle" size={24} color="#ef4444" />
                <Text style={styles.problemText}>
                  Povprečna družina zapravi{" "}
                  <Text style={styles.problemHighlight}>€200+ mesečno</Text>
                  {"\n"}preveč na hrani!
                </Text>
              </LinearGradient>
            </View>

            {/* CTA Buttons */}
            <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
              <TouchableOpacity
                style={styles.ctaButton}
                onPress={handleGetStarted}
                activeOpacity={0.9}
              >
                <LinearGradient
                  colors={["#10b981", "#059669", "#047857"]}
                  style={styles.ctaGradient}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                >
                  <Text style={styles.ctaText}>ZAČNI PRIHRANITI</Text>
                  <Ionicons name="arrow-forward" size={24} color="#fff" />
                </LinearGradient>
              </TouchableOpacity>
            </Animated.View>

            <TouchableOpacity
              style={styles.secondaryButton}
              onPress={handleLogin}
              activeOpacity={0.8}
            >
              <Text style={styles.secondaryButtonText}>Že imaš račun? Prijavi se</Text>
            </TouchableOpacity>

            {/* Trust indicators below CTA */}
            <View style={styles.trustRow}>
              {TRUST_BADGES.slice(0, 2).map((badge, idx) => (
                <View key={idx} style={styles.trustBadge}>
                  <Ionicons name={badge.icon as any} size={16} color="#10b981" />
                  <Text style={styles.trustText}>{badge.text}</Text>
                </View>
              ))}
            </View>
          </Animated.View>

          {/* SOCIAL PROOF - Statistics */}
          <Animated.View
            style={[
              styles.statsSection,
              {
                opacity: statsAnim,
                transform: [
                  {
                    translateY: statsAnim.interpolate({
                      inputRange: [0, 1],
                      outputRange: [50, 0],
                    }),
                  },
                ],
              },
            ]}
          >
            <Text style={styles.sectionTitle}>Slovenija že prihrani</Text>
            <View style={styles.statsGrid}>
              {STATS.map((stat, idx) => (
                <View key={idx} style={styles.statCard}>
                  <LinearGradient
                    colors={["rgba(139, 92, 246, 0.15)", "rgba(88, 28, 135, 0.1)"]}
                    style={styles.statGradient}
                  >
                    <Ionicons name={stat.icon as any} size={32} color="#a855f7" />
                    <Text style={styles.statValue}>{stat.value}</Text>
                    <Text style={styles.statLabel}>{stat.label}</Text>
                  </LinearGradient>
                </View>
              ))}
            </View>
          </Animated.View>

          {/* FEATURES SHOWCASE */}
          <View style={styles.featuresSection}>
            <Text style={styles.sectionTitle}>Zakaj Pr'Hran?</Text>
            <Text style={styles.sectionSubtitle}>
              Vse kar potrebuješ za pametno nakupovanje
            </Text>

            <View style={styles.featuresGrid}>
              {FEATURES.map((feature, idx) => (
                <View key={idx} style={styles.featureCard}>
                  <LinearGradient
                    colors={[...feature.gradient, feature.gradient[1] + "80"]}
                    style={styles.featureIconContainer}
                    start={{ x: 0, y: 0 }}
                    end={{ x: 1, y: 1 }}
                  >
                    <Ionicons name={feature.icon as any} size={32} color="#fff" />
                  </LinearGradient>
                  <Text style={styles.featureTitle}>{feature.title}</Text>
                  <Text style={styles.featureDescription}>{feature.description}</Text>
                </View>
              ))}
            </View>
          </View>

          {/* HOW IT WORKS */}
          <View style={styles.howSection}>
            <Text style={styles.sectionTitle}>Kako deluje?</Text>
            <Text style={styles.sectionSubtitle}>
              3 preprosti koraki do prihrankov
            </Text>

            <View style={styles.stepsContainer}>
              {HOW_IT_WORKS.map((step, idx) => (
                <View key={idx} style={styles.stepCard}>
                  <View style={styles.stepHeader}>
                    <View style={styles.stepNumber}>
                      <LinearGradient
                        colors={["#a855f7", "#7c3aed"]}
                        style={styles.stepNumberGradient}
                      >
                        <Text style={styles.stepNumberText}>{step.step}</Text>
                      </LinearGradient>
                    </View>
                    <View style={styles.stepContent}>
                      <Text style={styles.stepTitle}>{step.title}</Text>
                      <Text style={styles.stepDescription}>{step.description}</Text>
                    </View>
                    <View style={styles.stepIconContainer}>
                      <Ionicons name={step.icon as any} size={36} color="#a855f7" />
                    </View>
                  </View>
                  {idx < HOW_IT_WORKS.length - 1 && (
                    <View style={styles.stepConnector} />
                  )}
                </View>
              ))}
            </View>
          </View>

          {/* TRUST & SECURITY */}
          <View style={styles.trustSection}>
            <View style={styles.trustCard}>
              <LinearGradient
                colors={["rgba(34, 197, 94, 0.15)", "rgba(22, 163, 74, 0.1)"]}
                style={styles.trustCardGradient}
              >
                <Ionicons name="shield-checkmark" size={48} color="#22c55e" />
                <Text style={styles.trustCardTitle}>Varnost in zasebnost</Text>
                <Text style={styles.trustCardDescription}>
                  Tvoji podatki so varni. Brez prodaje podatkov tretjim osebam.
                  Brez skritih stroškov. 100% transparentno.
                </Text>
                <View style={styles.trustBadgesGrid}>
                  {TRUST_BADGES.map((badge, idx) => (
                    <View key={idx} style={styles.trustBadgeItem}>
                      <Ionicons name={badge.icon as any} size={20} color="#10b981" />
                      <Text style={styles.trustBadgeText}>{badge.text}</Text>
                    </View>
                  ))}
                </View>
              </LinearGradient>
            </View>
          </View>

          {/* FINAL CTA */}
          <View style={styles.finalCtaSection}>
            <Text style={styles.finalCtaTitle}>
              Pripravljeni prihraniti?
            </Text>
            <Text style={styles.finalCtaSubtitle}>
              Pridruži se tisočim Slovencem ki že varčujejo
            </Text>

            <TouchableOpacity
              style={styles.finalCtaButton}
              onPress={handleGetStarted}
              activeOpacity={0.9}
            >
              <LinearGradient
                colors={["#10b981", "#059669"]}
                style={styles.finalCtaGradient}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
              >
                <Text style={styles.finalCtaText}>ZAČNI ZASTONJ</Text>
                <Ionicons name="rocket" size={24} color="#fff" />
              </LinearGradient>
            </TouchableOpacity>

            <Text style={styles.finalCtaFooter}>
              Brez kreditne kartice. Brez obveznosti. Zastonj za vedno.
            </Text>
          </View>

          <View style={{ height: 60 }} />
        </ScrollView>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#0a0a12",
  },
  safeArea: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: 20,
    alignItems: "center",
  },
  bgIcon: {
    position: "absolute",
    zIndex: 0,
  },
  bgIconTopLeft: {
    top: -20,
    left: -40,
  },
  bgIconBottomRight: {
    bottom: 100,
    right: -30,
  },

  // HERO SECTION
  heroSection: {
    alignItems: "center",
    paddingTop: 40,
    paddingBottom: 60,
    width: "100%",
    maxWidth: 600,
  },
  heroTitle: {
    fontSize: 42,
    fontWeight: "900",
    color: "#fff",
    textAlign: "center",
    marginTop: 32,
    lineHeight: 50,
    letterSpacing: -1,
  },
  heroTitleAccent: {
    color: "#22c55e",
  },
  heroSubtitle: {
    fontSize: 20,
    color: "#d1d5db",
    textAlign: "center",
    marginTop: 16,
    lineHeight: 28,
    maxWidth: 500,
  },
  boldText: {
    fontWeight: "800",
    color: "#fff",
  },
  problemCard: {
    marginTop: 32,
    borderRadius: 20,
    overflow: "hidden",
    width: "100%",
    maxWidth: 500,
  },
  problemGradient: {
    flexDirection: "row",
    alignItems: "center",
    padding: 20,
    gap: 16,
    borderWidth: 1,
    borderColor: "rgba(239, 68, 68, 0.3)",
  },
  problemText: {
    flex: 1,
    fontSize: 16,
    color: "#fca5a5",
    lineHeight: 24,
    fontWeight: "600",
  },
  problemHighlight: {
    fontSize: 18,
    fontWeight: "900",
    color: "#ef4444",
  },
  ctaButton: {
    marginTop: 32,
    borderRadius: 30,
    overflow: "hidden",
    width: "100%",
    maxWidth: 400,
    ...createShadow("#10b981", 0, 12, 0.6, 24, 16),
  },
  ctaGradient: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 20,
    paddingHorizontal: 40,
    gap: 12,
  },
  ctaText: {
    fontSize: 20,
    fontWeight: "900",
    color: "#fff",
    letterSpacing: 1,
  },
  secondaryButton: {
    marginTop: 16,
    paddingVertical: 12,
  },
  secondaryButtonText: {
    fontSize: 16,
    color: "#a78bfa",
    fontWeight: "600",
  },
  trustRow: {
    flexDirection: "row",
    gap: 24,
    marginTop: 24,
    flexWrap: "wrap",
    justifyContent: "center",
  },
  trustBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  trustText: {
    fontSize: 14,
    color: "#9ca3af",
    fontWeight: "600",
  },

  // STATS SECTION
  statsSection: {
    width: "100%",
    maxWidth: 1000,
    marginBottom: 80,
  },
  sectionTitle: {
    fontSize: 32,
    fontWeight: "900",
    color: "#fff",
    textAlign: "center",
    marginBottom: 16,
    letterSpacing: -0.5,
  },
  sectionSubtitle: {
    fontSize: 18,
    color: "#9ca3af",
    textAlign: "center",
    marginBottom: 32,
    lineHeight: 26,
  },
  statsGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 20,
    justifyContent: "center",
  },
  statCard: {
    width: SCREEN_WIDTH > 768 ? 280 : (SCREEN_WIDTH - 60) / 2,
    minWidth: 150,
    borderRadius: 20,
    overflow: "hidden",
  },
  statGradient: {
    padding: 24,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "rgba(139, 92, 246, 0.3)",
    minHeight: 160,
    justifyContent: "center",
  },
  statValue: {
    fontSize: 36,
    fontWeight: "900",
    color: "#a855f7",
    marginTop: 16,
  },
  statLabel: {
    fontSize: 14,
    color: "#d1d5db",
    marginTop: 8,
    textAlign: "center",
    fontWeight: "600",
  },

  // FEATURES SECTION
  featuresSection: {
    width: "100%",
    maxWidth: 1000,
    marginBottom: 80,
  },
  featuresGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 20,
    justifyContent: "center",
  },
  featureCard: {
    width: SCREEN_WIDTH > 768 ? 220 : (SCREEN_WIDTH - 60) / 2,
    minWidth: 160,
    backgroundColor: "rgba(139, 92, 246, 0.08)",
    borderRadius: 20,
    padding: 24,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "rgba(139, 92, 246, 0.2)",
  },
  featureIconContainer: {
    width: 72,
    height: 72,
    borderRadius: 36,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 16,
  },
  featureTitle: {
    fontSize: 18,
    fontWeight: "800",
    color: "#fff",
    textAlign: "center",
    marginBottom: 8,
  },
  featureDescription: {
    fontSize: 14,
    color: "#9ca3af",
    textAlign: "center",
    lineHeight: 20,
  },

  // HOW IT WORKS
  howSection: {
    width: "100%",
    maxWidth: 700,
    marginBottom: 80,
  },
  stepsContainer: {
    width: "100%",
  },
  stepCard: {
    marginBottom: 16,
  },
  stepHeader: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(139, 92, 246, 0.08)",
    borderRadius: 20,
    padding: 20,
    borderWidth: 1,
    borderColor: "rgba(139, 92, 246, 0.2)",
    gap: 16,
  },
  stepNumber: {
    borderRadius: 30,
    overflow: "hidden",
  },
  stepNumberGradient: {
    width: 60,
    height: 60,
    alignItems: "center",
    justifyContent: "center",
  },
  stepNumberText: {
    fontSize: 28,
    fontWeight: "900",
    color: "#fff",
  },
  stepContent: {
    flex: 1,
  },
  stepTitle: {
    fontSize: 20,
    fontWeight: "800",
    color: "#fff",
    marginBottom: 4,
  },
  stepDescription: {
    fontSize: 14,
    color: "#9ca3af",
    lineHeight: 20,
  },
  stepIconContainer: {
    width: 56,
    height: 56,
    alignItems: "center",
    justifyContent: "center",
  },
  stepConnector: {
    width: 2,
    height: 24,
    backgroundColor: "rgba(139, 92, 246, 0.3)",
    marginLeft: 30,
    marginVertical: 4,
  },

  // TRUST SECTION
  trustSection: {
    width: "100%",
    maxWidth: 700,
    marginBottom: 80,
  },
  trustCard: {
    borderRadius: 24,
    overflow: "hidden",
  },
  trustCardGradient: {
    padding: 32,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "rgba(34, 197, 94, 0.3)",
  },
  trustCardTitle: {
    fontSize: 24,
    fontWeight: "900",
    color: "#22c55e",
    marginTop: 16,
    marginBottom: 12,
  },
  trustCardDescription: {
    fontSize: 16,
    color: "#d1d5db",
    textAlign: "center",
    lineHeight: 24,
    marginBottom: 24,
  },
  trustBadgesGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 16,
    justifyContent: "center",
  },
  trustBadgeItem: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    backgroundColor: "rgba(16, 185, 129, 0.1)",
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "rgba(16, 185, 129, 0.3)",
  },
  trustBadgeText: {
    fontSize: 14,
    color: "#10b981",
    fontWeight: "700",
  },

  // FINAL CTA
  finalCtaSection: {
    width: "100%",
    maxWidth: 600,
    alignItems: "center",
    paddingVertical: 40,
  },
  finalCtaTitle: {
    fontSize: 36,
    fontWeight: "900",
    color: "#fff",
    textAlign: "center",
    marginBottom: 12,
  },
  finalCtaSubtitle: {
    fontSize: 18,
    color: "#9ca3af",
    textAlign: "center",
    marginBottom: 32,
  },
  finalCtaButton: {
    width: "100%",
    maxWidth: 400,
    borderRadius: 30,
    overflow: "hidden",
    ...createShadow("#10b981", 0, 16, 0.7, 32, 20),
  },
  finalCtaGradient: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 22,
    paddingHorizontal: 40,
    gap: 16,
  },
  finalCtaText: {
    fontSize: 22,
    fontWeight: "900",
    color: "#fff",
    letterSpacing: 1,
  },
  finalCtaFooter: {
    fontSize: 14,
    color: "#6b7280",
    textAlign: "center",
    marginTop: 16,
    fontStyle: "italic",
  },
});

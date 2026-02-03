import { useState, useEffect } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Dimensions,
  Platform,
  StatusBar,
  Image,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import * as Haptics from "expo-haptics";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { BlurView } from "expo-blur";
import Animated, {
  useAnimatedScrollHandler,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withSequence,
  withSpring,
  withTiming,
  interpolate,
  Extrapolate,
} from "react-native-reanimated";
import Logo from "../lib/Logo";

const { width: SCREEN_WIDTH } = Dimensions.get("window");

// --- DATA ---
// Vsi podatki so v slovenščini, kot zahtevano.

const TRUST_METRICS = [
  { value: "14.230€", label: "DANES PRIHRANJENO" },
  { value: "5.000+", label: "UPORABNIKOV" },
  { value: "4.9/5", label: "OCENA" },
];

const REVIEWS = [
  {
    name: "Ana K.",
    role: "Maribor",
    text: "Končno vem kje je Barilla najcenejša. Prihranila 30€ ta teden!",
    stars: 5,
  },
  {
    name: "Tomaž N.",
    role: "Ljubljana",
    text: "Top aplikacija. Prhran Family uporabljamo vsi doma.",
    stars: 5,
  },
  {
    name: "Maja Z.",
    role: "Celje",
    text: "Vsak mesec mi ostane za eno polno košarico denarja. Hvala!",
    stars: 5,
  },
];

const FEATURES = [
  {
    icon: "scan",
    title: "Skeniraj in Primerjaj",
    desc: "Slikaj izdelek in takoj ugotovi, kje je cenejši.",
  },
  {
    icon: "cart",
    title: "Pametna Košarica",
    desc: "Naredi seznam, mi ti povemo v katero trgovino se splača.",
  },
  {
    icon: "notifications",
    title: "Obvestila o Akcijah",
    desc: "Ne zamudi, ko tvoj najljubši izdelek znižajo.",
  },
];

// --- COMPONENTS ---

const AnimatedBlurView = Animated.createAnimatedComponent(BlurView);
const AnimatedLinearGradient = Animated.createAnimatedComponent(LinearGradient);

export default function OnboardingScreen() {
  const router = useRouter();
  const scrollY = useSharedValue(0);
  const heroOpacity = useSharedValue(0);
  const heroScale = useSharedValue(0.9);
  const glowPulse = useSharedValue(0.6);

  // Initial animations
  useEffect(() => {
    heroOpacity.value = withTiming(1, { duration: 1000 });
    heroScale.value = withSpring(1, { damping: 12 });
    glowPulse.value = withRepeat(
      withSequence(
        withTiming(0.8, { duration: 2000 }),
        withTiming(0.6, { duration: 2000 })
      ),
      -1,
      true
    );

    // Mark onboarding as seen immediately (simpler flow)
    AsyncStorage.setItem("prhran_onboarding_completed", "true").catch(console.error);
  }, []);

  const scrollHandler = useAnimatedScrollHandler({
    onScroll: (event) => {
      scrollY.value = event.contentOffset.y;
    },
  });

  const triggerHaptic = () => {
    if (Platform.OS !== "web") Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };

  const handleAction = () => {
    triggerHaptic();
    // Redirect to auth directly
    router.push("/auth?mode=register");
  };

  const handleLogin = () => {
    triggerHaptic();
    router.push("/auth?mode=login");
  };

  // --- ANIMATED STYLES ---

  const heroStyle = useAnimatedStyle(() => {
    return {
      opacity: heroOpacity.value,
      transform: [
        { scale: heroScale.value },
        { translateY: interpolate(scrollY.value, [0, 300], [0, 100], Extrapolate.CLAMP) },
      ],
    };
  });

  const glowStyle = useAnimatedStyle(() => {
    return {
      opacity: glowPulse.value,
      transform: [
        { scale: interpolate(glowPulse.value, [0.6, 0.8], [1, 1.2]) },
      ],
    };
  });

  const stickyHeaderStyle = useAnimatedStyle(() => {
    const opacity = interpolate(scrollY.value, [100, 200], [0, 1], Extrapolate.CLAMP);
    return {
      opacity,
      pointerEvents: opacity > 0.5 ? "auto" : "none",
    };
  });

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />

      {/* BACKGROUND */}
      <View style={styles.backgroundContainer}>
        <LinearGradient
          colors={["#0a0a12", "#12081f", "#1a0a2e", "#270a3a", "#0f0a1e"]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={StyleSheet.absoluteFill}
        />
        {/* Animated Glow in Center */}
        <AnimatedLinearGradient
          colors={["rgba(168, 85, 247, 0.4)", "transparent"]}
          style={[styles.glowOrb, glowStyle]}
          start={{ x: 0.5, y: 0.5 }}
          end={{ x: 1, y: 1 }}
        />
      </View>

      {/* NAVBAR */}
      <SafeAreaView edges={['top']} style={styles.navbarSafeArea}>
        <View style={styles.navbar}>
          <View style={styles.navLeft}>
            <Logo size={32} />
            <Text style={styles.navLogoText}>Pr'Hran</Text>
          </View>
          <View style={styles.navRight}>
            <TouchableOpacity onPress={handleLogin} style={styles.navBtnLink}>
              <Text style={styles.navBtnLinkText}>Prijava</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={handleAction} style={styles.navBtnPrimary}>
              <Text style={styles.navBtnPrimaryText}>Registracija</Text>
            </TouchableOpacity>
          </View>
        </View>
      </SafeAreaView>

      {/* STICKY HEADER (Appears on scroll) */}
      <AnimatedBlurView intensity={50} tint="dark" style={[styles.stickyHeader, stickyHeaderStyle]}>
        <SafeAreaView edges={['top']} style={styles.stickyContent}>
          <View style={styles.stickyInner}>
            <Text style={styles.stickyTitle}>Pr'Hran</Text>
            <TouchableOpacity onPress={handleAction} style={styles.stickyBtn}>
              <Text style={styles.stickyBtnText}>Začni Zastonj</Text>
            </TouchableOpacity>
          </View>
        </SafeAreaView>
      </AnimatedBlurView>

      {/* SCROLL CONTENT */}
      <Animated.ScrollView
        onScroll={scrollHandler}
        scrollEventThrottle={16}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        <SafeAreaView edges={['top']} style={{ flex: 1 }}>

          {/* 1. HERO SECTION */}
          <Animated.View style={[styles.heroSection, heroStyle]}>
            {/* Live Badge */}
            <View style={styles.liveBadgeWrapper}>
              <BlurView intensity={30} tint="dark" style={styles.liveBadge}>
                <View style={styles.liveDot} />
                <Text style={styles.liveText}>V ŽIVO | <Text style={styles.liveCount}>2,847</Text> Slovencev varčuje</Text>
              </BlurView>
            </View>

            <Text style={styles.heroTitle}>
              Nakupuj Pametno.{"\n"}
              <Text style={styles.heroTitleGradient}>Prihrani Takoj.</Text>
            </Text>

            <Text style={styles.heroSubtitle}>
              Prva slovenska AI aplikacija za primerjavo cen živil.{"\n"}
              Ne meči denarja stran v napačni trgovini.
            </Text>

            <View style={styles.heroButtons}>
              <TouchableOpacity
                onPress={handleAction}
                activeOpacity={0.8}
                style={styles.heroMainBtn}
              >
                <LinearGradient
                  colors={["#a855f7", "#7c3aed"]} // Purple gradient like ExamAi
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 1 }}
                  style={styles.heroMainBtnGradient}
                >
                  <Text style={styles.heroMainBtnText}>Ustvari Račun</Text>
                  <Ionicons name="arrow-forward" size={24} color="white" />
                </LinearGradient>
              </TouchableOpacity>
            </View>

            {/* Platform Badges */}
            <Text style={styles.platformText}>Kmalu na voljo za iOS in Android</Text>
          </Animated.View>

          <View style={styles.spacer} />

          {/* 2. STATS BAR */}
          <View style={styles.statsRow}>
            {TRUST_METRICS.map((item, index) => (
              <View key={index} style={styles.statItem}>
                <Text style={styles.statValue}>{item.value}</Text>
                <Text style={styles.statLabel}>{item.label}</Text>
              </View>
            ))}
          </View>

          <View style={styles.spacerLarge} />

          {/* 3. LOSS AVERSION (Red vs Green) */}
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Zakaj plačati več?</Text>
            <Text style={styles.sectionSub}>Ista košarica, ogromna razlika.</Text>
          </View>

          <View style={styles.comparisonContainer}>
            {/* The "Bad" Way */}
            <View style={[styles.compareCard, styles.compareCardBad]}>
              <View style={styles.compareHeaderBad}>
                <Ionicons name="close-circle" size={24} color="#ef4444" />
                <Text style={styles.compareTitleBad}>Naključni Nakup</Text>
              </View>
              <View style={styles.receiptLine}><Text style={styles.receiptText}>Mleko 1L</Text><Text style={styles.receiptPrice}>1.49€</Text></View>
              <View style={styles.receiptLine}><Text style={styles.receiptText}>Testenine</Text><Text style={styles.receiptPrice}>1.29€</Text></View>
              <View style={styles.receiptLine}><Text style={styles.receiptText}>Tuna</Text><Text style={styles.receiptPrice}>2.89€</Text></View>
              <View style={styles.receiptLine}><Text style={styles.receiptText}>Kava</Text><Text style={styles.receiptPrice}>6.99€</Text></View>
              <View style={styles.divider} />
              <View style={styles.receiptTotal}>
                <Text style={styles.totalLabel}>Skupaj:</Text>
                <Text style={styles.totalPriceBad}>12.66€</Text>
              </View>
            </View>

            {/* The "Good" Way */}
            <View style={[styles.compareCard, styles.compareCardGood]}>
              <View style={styles.compareHeaderGood}>
                <Ionicons name="checkmark-circle" size={24} color="#10b981" />
                <Text style={styles.compareTitleGood}>Pr'Hran Nakup</Text>
              </View>
              <View style={styles.receiptLine}><Text style={styles.receiptText}>Mleko 1L</Text><Text style={styles.receiptPrice}>0.99€</Text></View>
              <View style={styles.receiptLine}><Text style={styles.receiptText}>Testenine</Text><Text style={styles.receiptPrice}>0.89€</Text></View>
              <View style={styles.receiptLine}><Text style={styles.receiptText}>Tuna</Text><Text style={styles.receiptPrice}>1.99€</Text></View>
              <View style={styles.receiptLine}><Text style={styles.receiptText}>Kava</Text><Text style={styles.receiptPrice}>4.99€</Text></View>
              <View style={styles.divider} />
              <View style={styles.receiptTotal}>
                <Text style={styles.totalLabel}>Skupaj:</Text>
                <Text style={styles.totalPriceGood}>8.86€</Text>
              </View>
              <View style={styles.savingsTag}>
                <Text style={styles.savingsText}>Prihranek: 3.80€</Text>
              </View>
            </View>
          </View>

          <View style={styles.spacerLarge} />

          {/* 4. PREMIUM TIERS TEASER */}
          <View style={styles.premiumTeaser}>
            <LinearGradient
              colors={["rgba(139, 92, 246, 0.1)", "rgba(139, 92, 246, 0.05)"]}
              style={styles.premiumTeaserGradient}
            >
              <View style={styles.premiumBadge}>
                <Ionicons name="diamond" size={16} color="#fbbf24" />
                <Text style={styles.premiumBadgeText}>NOVO</Text>
              </View>
              <Text style={styles.premiumTitle}>Več kot le prihranki</Text>
              <Text style={styles.premiumDesc}>
                Odkrij <Text style={{ color: "#a855f7", fontWeight: "700" }}>Pr'Hran PLUS</Text> za neomejeno iskanje ali{" "}
                <Text style={{ color: "#f59e0b", fontWeight: "700" }}>Pr'Hran Family</Text> za
                skupno varčevanje s partnerjem ali družino (do 3 osebe).
              </Text>
              <View style={styles.premiumFeaturesRow}>
                <View style={styles.premFeat}><Ionicons name="infinite" size={16} color="#a855f7" /><Text style={styles.premFeatText}>Neomejeno</Text></View>
                <View style={styles.premFeat}><Ionicons name="people" size={16} color="#f59e0b" /><Text style={styles.premFeatText}>Družina</Text></View>
                <View style={styles.premFeat}><Ionicons name="trophy" size={16} color="#22c55e" /><Text style={styles.premFeatText}>Nagrade</Text></View>
              </View>
            </LinearGradient>
          </View>

          <View style={styles.spacerLarge} />

          {/* 5. REVIEWS / SOCIAL PROOF */}
          <View style={styles.reviewsSection}>
            <Text style={styles.sectionTitle}>Mnenja Uporabnikov</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.reviewsScroll}>
              {REVIEWS.map((review, i) => (
                <View key={i} style={styles.reviewCard}>
                  <View style={styles.reviewHeader}>
                    <View style={styles.avatarPlaceholder}><Text style={styles.avatarText}>{review.name[0]}</Text></View>
                    <View>
                      <Text style={styles.reviewName}>{review.name}</Text>
                      <Text style={styles.reviewRole}>{review.role}</Text>
                    </View>
                  </View>
                  <Text style={styles.reviewText}>"{review.text}"</Text>
                  <View style={styles.starsRow}>
                    {[...Array(5)].map((_, j) => (
                      <Ionicons key={j} name="star" size={14} color="#fbbf24" />
                    ))}
                  </View>
                </View>
              ))}
            </ScrollView>
          </View>

          <View style={styles.spacerLarge} />

          {/* 6. BOTTOM CTA */}
          <View style={styles.bottomCta}>
            <LinearGradient
              colors={["#120a21", "#2e1065"]}
              style={styles.bottomCtaGradient}
            >
              <Text style={styles.bottomCtaTitle}>Začni varčevati danes.</Text>
              <Text style={styles.bottomCtaSub}>Brezplačno. Enostavno. Slovensko.</Text>
              <TouchableOpacity onPress={handleAction} style={styles.whiteBtn}>
                <Text style={styles.whiteBtnText}>Začni Zastonj</Text>
                <Ionicons name="arrow-forward" size={20} color="#120a21" />
              </TouchableOpacity>
            </LinearGradient>
          </View>

          <View style={{ height: 100 }} />

        </SafeAreaView>
      </Animated.ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#050508",
  },
  backgroundContainer: {
    ...StyleSheet.absoluteFillObject,
    zIndex: -1,
    overflow: "hidden",
  },
  glowOrb: {
    position: "absolute",
    width: SCREEN_WIDTH * 1.5,
    height: SCREEN_WIDTH * 1.5,
    borderRadius: SCREEN_WIDTH,
    top: -SCREEN_WIDTH * 0.5,
    left: -SCREEN_WIDTH * 0.25,
  },

  // NAVBAR
  navbarSafeArea: {
    zIndex: 10,
  },
  navbar: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
    paddingVertical: 10,
    height: 60,
  },
  navLeft: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  navLogoText: {
    color: "#fff",
    fontWeight: "700",
    fontSize: 20,
    letterSpacing: 0.5,
  },
  navRight: {
    flexDirection: "row",
    gap: 12,
    alignItems: "center",
  },
  navBtnLink: {
    paddingVertical: 8,
    paddingHorizontal: 12,
  },
  navBtnLinkText: {
    color: "#cbd5e1",
    fontSize: 15,
    fontWeight: "500",
  },
  navBtnPrimary: {
    backgroundColor: "#2e1065",
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "#4c1d95",
  },
  navBtnPrimaryText: {
    color: "#fff",
    fontSize: 14,
    fontWeight: "600",
  },

  // STICKY HEADER
  stickyHeader: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    padding: 0,
    zIndex: 100,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(255,255,255,0.1)",
  },
  stickyContent: {
    backgroundColor: "transparent",
  },
  stickyInner: {
    height: 60,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
  },
  stickyTitle: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "bold",
  },
  stickyBtn: {
    backgroundColor: "#a855f7",
    paddingVertical: 8,
    paddingHorizontal: 20,
    borderRadius: 20,
  },
  stickyBtnText: {
    color: "#fff",
    fontWeight: "700",
    fontSize: 14,
  },

  // SCROLL CONTENT
  scrollContent: {
    paddingBottom: 40,
  },
  spacer: { height: 40 },
  spacerLarge: { height: 80 },

  // HERO
  heroSection: {
    alignItems: "center",
    paddingHorizontal: 20,
    paddingTop: 40,
  },
  liveBadgeWrapper: {
    marginBottom: 24,
    borderRadius: 20,
    overflow: "hidden",
    borderWidth: 1,
    borderColor: "rgba(16, 185, 129, 0.3)",
  },
  liveBadge: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 8,
    gap: 8,
    backgroundColor: "rgba(5, 40, 20, 0.4)",
  },
  liveDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: "#10b981",
  },
  liveText: {
    color: "#a7f3d0",
    fontSize: 13,
    fontWeight: "500",
  },
  liveCount: {
    color: "#fff",
    fontWeight: "700",
  },
  heroTitle: {
    fontSize: 38,
    lineHeight: 46,
    color: "#fff",
    fontWeight: "800",
    textAlign: "center",
    marginBottom: 16,
  },
  heroTitleGradient: {
    color: "#c084fc", // Fallback
  },
  heroSubtitle: {
    fontSize: 16,
    lineHeight: 24,
    color: "#94a3b8",
    textAlign: "center",
    maxWidth: 320,
    marginBottom: 32,
  },
  heroButtons: {
    width: "100%",
    alignItems: "center",
    marginBottom: 24,
  },
  heroMainBtn: {
    width: "100%",
    maxWidth: 300,
    borderRadius: 32,
    shadowColor: "#a855f7",
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.4,
    shadowRadius: 20,
    elevation: 10,
  },
  heroMainBtnGradient: {
    paddingVertical: 18,
    paddingHorizontal: 32,
    borderRadius: 32,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 12,
  },
  heroMainBtnText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "700",
  },
  platformText: {
    color: "#64748b",
    fontSize: 12,
    marginTop: 8,
  },

  // STATS
  statsRow: {
    flexDirection: "row",
    justifyContent: "space-around",
    paddingHorizontal: 10,
    width: "100%",
    maxWidth: 500,
    alignSelf: "center",
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: "rgba(255,255,255,0.05)",
    paddingVertical: 20,
    backgroundColor: "rgba(255,255,255,0.02)",
  },
  statItem: {
    alignItems: "center",
  },
  statValue: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "700",
    marginBottom: 4,
  },
  statLabel: {
    color: "#94a3b8",
    fontSize: 10,
    textTransform: "uppercase",
    letterSpacing: 1,
  },

  // SECTIONS
  sectionHeader: {
    alignItems: "center",
    marginBottom: 32,
    paddingHorizontal: 20,
  },
  sectionTitle: {
    color: "#fff",
    fontSize: 26,
    fontWeight: "700",
    textAlign: "center",
    marginBottom: 8,
  },
  sectionSub: {
    color: "#94a3b8",
    fontSize: 15,
    textAlign: "center",
  },

  // COMPARISON
  comparisonContainer: {
    flexDirection: SCREEN_WIDTH > 600 ? "row" : "column",
    gap: 20,
    paddingHorizontal: 20,
    maxWidth: 800,
    alignSelf: "center",
    width: "100%",
  },
  compareCard: {
    flex: 1,
    backgroundColor: "#1e1e24",
    borderRadius: 20,
    padding: 20,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.1)",
  },
  compareCardBad: {
    backgroundColor: "rgba(239, 68, 68, 0.05)",
    borderColor: "rgba(239, 68, 68, 0.2)",
  },
  compareCardGood: {
    backgroundColor: "rgba(16, 185, 129, 0.05)",
    borderColor: "rgba(16, 185, 129, 0.2)",
    transform: [{ scale: 1.02 }],
    zIndex: 2,
    shadowColor: "#10b981",
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.2,
    shadowRadius: 20,
  },
  compareHeaderBad: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 20,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(239, 68, 68, 0.2)",
  },
  compareTitleBad: { color: "#fca5a5", fontSize: 16, fontWeight: "700" },

  compareHeaderGood: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 20,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(16, 185, 129, 0.2)",
  },
  compareTitleGood: { color: "#6ee7b7", fontSize: 16, fontWeight: "700" },

  receiptLine: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 12,
  },
  receiptText: { color: "#cbd5e1", fontSize: 14 },
  receiptPrice: { color: "#fff", fontWeight: "600", fontSize: 14 },
  divider: { height: 1, backgroundColor: "rgba(255,255,255,0.1)", marginVertical: 12 },
  receiptTotal: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-end",
  },
  totalLabel: { color: "#94a3b8", fontSize: 14 },
  totalPriceBad: { color: "#ef4444", fontSize: 22, fontWeight: "700" },
  totalPriceGood: { color: "#10b981", fontSize: 22, fontWeight: "700" },
  savingsTag: {
    marginTop: 12,
    backgroundColor: "rgba(16, 185, 129, 0.2)",
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 8,
    alignSelf: "flex-end",
  },
  savingsText: { color: "#34d399", fontWeight: "700", fontSize: 12 },

  // PREMIUM TEASER
  premiumTeaser: {
    marginHorizontal: 20,
    borderRadius: 20,
    overflow: "hidden",
    borderWidth: 1,
    borderColor: "rgba(139, 92, 246, 0.3)",
  },
  premiumTeaserGradient: {
    padding: 24,
    alignItems: "center",
  },
  premiumBadge: {
    flexDirection: "row",
    gap: 6,
    backgroundColor: "rgba(251, 191, 36, 0.1)",
    paddingVertical: 4,
    paddingHorizontal: 10,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: "rgba(251, 191, 36, 0.3)",
  },
  premiumBadgeText: { color: "#fbbf24", fontWeight: "700", fontSize: 10 },
  premiumTitle: { color: "#fff", fontSize: 22, fontWeight: "700", marginBottom: 8 },
  premiumDesc: { color: "#cbd5e1", fontSize: 14, textAlign: "center", lineHeight: 22, marginBottom: 16 },
  premiumFeaturesRow: { flexDirection: "row", gap: 16, flexWrap: "wrap", justifyContent: "center" },
  premFeat: { flexDirection: "row", gap: 6, alignItems: "center", backgroundColor: "#0f0a1e", padding: 8, borderRadius: 8 },
  premFeatText: { color: "#fff", fontSize: 12, fontWeight: "600" },

  // REVIEWS
  reviewsSection: {},
  reviewsScroll: {
    paddingHorizontal: 20,
    gap: 16,
    paddingBottom: 20,
  },
  reviewCard: {
    width: 260,
    backgroundColor: "#18181b",
    padding: 20,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.05)",
  },
  reviewHeader: {
    flexDirection: "row",
    gap: 12,
    alignItems: "center",
    marginBottom: 12,
  },
  avatarPlaceholder: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: "#3f3f46",
    alignItems: "center",
    justifyContent: "center",
  },
  avatarText: { color: "#fff", fontWeight: "700" },
  reviewName: { color: "#fff", fontWeight: "600", fontSize: 14 },
  reviewRole: { color: "#71717a", fontSize: 12 },
  reviewText: { color: "#d4d4d8", fontSize: 13, lineHeight: 20, height: 60 },
  starsRow: { flexDirection: "row", gap: 2, marginTop: 12 },

  // BOTTOM CTA
  bottomCta: {
    marginHorizontal: 20,
    borderRadius: 30,
    overflow: "hidden",
  },
  bottomCtaGradient: {
    padding: 32,
    alignItems: "center",
  },
  bottomCtaTitle: {
    color: "#fff",
    fontSize: 24,
    fontWeight: "800",
    textAlign: "center",
    marginBottom: 8,
  },
  bottomCtaSub: {
    color: "#c4b5fd",
    fontSize: 14,
    marginBottom: 24,
    textAlign: "center",
  },
  whiteBtn: {
    backgroundColor: "#fff",
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    paddingVertical: 14,
    paddingHorizontal: 28,
    borderRadius: 30,
  },
  whiteBtnText: {
    color: "#120a21",
    fontWeight: "700",
    fontSize: 15,
  },
});

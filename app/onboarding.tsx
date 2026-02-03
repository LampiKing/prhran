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
  TextInput,
  Modal,
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
  withDelay,
  interpolate,
  Extrapolate,
  FadeInUp,
  FadeIn,
  FadeOut,
} from "react-native-reanimated";
import Logo from "../lib/Logo";

const { width: SCREEN_WIDTH } = Dimensions.get("window");

// --- DATA ---
const REVIEWS = [
  { name: "Marko", text: "Čuj toto je puno dobro. Prihranil 20€ na mesu ta teden.", stars: 4 },
  { name: "Nina", text: "Zakon zadeva! Ne rabim več listat tistih papirnatih katalogov", stars: 5 },
  { name: "Janja", text: "Meni je okej, samo včasih so cene v Tušu drugačne kot na polici", stars: 3 },
  { name: "Rok", text: "Top šit aplikacija. Skeniraš in vidiš kje te nategujejo s cenami", stars: 5 },
  { name: "Maja", text: "Family paket je super, da mama s tipom skupno listo", stars: 5 },
  { name: "Luka", text: "Dobra stvar, sam bi lahko blo več trgovin. Zaenkrat pa dela", stars: 3 },
  { name: "Sara", text: "Končno vem kje je Nutella najcenejša", stars: 5 },
  { name: "Matej", text: "Včasih se mi nelub pisat pa sam poskeniram pa najde takoj", stars: 4 },
  { name: "Ana", text: "Vsak teden prihranim vsaj 15€ in ogromno časa", stars: 5 },
  { name: "Tomaž", text: "Ful dobra aplikacija lahk bi dal še kako trgovino zravn", stars: 4 },
];

const TRUST_METRICS = [
  { value: "4365€", label: "PRIHRANJENO" },
  { value: "1.102", label: "UPORABNIKOV" },
  { value: "4.3", label: "OCENA" },
];

// --- EPIC PHONE ANIMATION ---
function EpicPhoneDemo() {
  const [step, setStep] = useState(0); // 0: search, 1: results, 2: added, 3: savings
  const searchOpacity = useSharedValue(1);
  const resultsOpacity = useSharedValue(0);
  const addedOpacity = useSharedValue(0);
  const savingsOpacity = useSharedValue(0);
  const typingProgress = useSharedValue(0);

  useEffect(() => {
    const sequence = async () => {
      // Step 0: Typing "Mleko"
      setStep(0);
      searchOpacity.value = 1;
      resultsOpacity.value = 0;
      addedOpacity.value = 0;
      savingsOpacity.value = 0;
      typingProgress.value = 0;
      typingProgress.value = withTiming(1, { duration: 1500 });

      await new Promise(r => setTimeout(r, 2000));

      // Step 1: Show results
      setStep(1);
      searchOpacity.value = withTiming(0, { duration: 300 });
      resultsOpacity.value = withTiming(1, { duration: 400 });

      await new Promise(r => setTimeout(r, 2500));

      // Step 2: Added to cart
      setStep(2);
      resultsOpacity.value = withTiming(0, { duration: 300 });
      addedOpacity.value = withTiming(1, { duration: 400 });

      await new Promise(r => setTimeout(r, 1500));

      // Step 3: Show savings
      setStep(3);
      addedOpacity.value = withTiming(0, { duration: 300 });
      savingsOpacity.value = withTiming(1, { duration: 400 });

      await new Promise(r => setTimeout(r, 2000));

      // Loop
      sequence();
    };

    sequence();
  }, []);

  const searchStyle = useAnimatedStyle(() => ({ opacity: searchOpacity.value }));
  const resultsStyle = useAnimatedStyle(() => ({ opacity: resultsOpacity.value }));
  const addedStyle = useAnimatedStyle(() => ({ opacity: addedOpacity.value }));
  const savingsStyle = useAnimatedStyle(() => ({ opacity: savingsOpacity.value }));

  const typedText = step === 0 ? "Mleko".substring(0, Math.floor(typingProgress.value * 5)) : "Mleko";

  return (
    <View style={styles.phoneFrame}>
      <View style={styles.phoneNotch} />
      <View style={styles.phoneContent}>

        {/* Step 0: Search Input */}
        <Animated.View style={[styles.demoStep, searchStyle, { position: 'absolute', top: 60, left: 0, right: 0 }]}>
          <View style={styles.searchBar}>
            <Ionicons name="search" size={18} color="#9ca3af" />
            <Text style={styles.searchText}>{typedText}</Text>
            <View style={styles.searchCursor} />
          </View>
        </Animated.View>

        {/* Step 1: Results */}
        <Animated.View style={[styles.demoStep, resultsStyle, { position: 'absolute', top: 40, left: 0, right: 0 }]}>
          <View style={styles.resultCard}>
            <View style={styles.resultHeader}>
              <Ionicons name="nutrition" size={20} color="#fff" />
              <Text style={styles.resultTitle}>Mleko 1L</Text>
            </View>
            <View style={styles.priceRow}>
              <View style={styles.priceItemGood}>
                <Text style={styles.storeName}>TUŠ</Text>
                <Text style={styles.priceGood}>0.99 €</Text>
              </View>
              <View style={styles.priceItemBad}>
                <Text style={styles.storeName}>MERCATOR</Text>
                <Text style={styles.priceBad}>1.49 €</Text>
              </View>
            </View>
            <TouchableOpacity style={styles.addBtn}>
              <Text style={styles.addBtnText}>Dodaj v seznam</Text>
            </TouchableOpacity>
          </View>
        </Animated.View>

        {/* Step 2: Added Confirmation */}
        <Animated.View style={[styles.demoStep, addedStyle, { position: 'absolute', top: 100, left: 0, right: 0, alignItems: 'center' }]}>
          <View style={styles.addedCard}>
            <View style={styles.checkCircle}>
              <Ionicons name="checkmark" size={32} color="#22c55e" />
            </View>
            <Text style={styles.addedTitle}>Dodano!</Text>
            <Text style={styles.addedSub}>Mleko 1L → Seznam</Text>
          </View>
        </Animated.View>

        {/* Step 3: Savings Display */}
        <Animated.View style={[styles.demoStep, savingsStyle, { position: 'absolute', top: 80, left: 0, right: 0 }]}>
          <View style={styles.savingsCard}>
            <Text style={styles.savingsLabel}>Prihranek</Text>
            <Text style={styles.savingsAmount}>0.50 €</Text>
            <Text style={styles.savingsSub}>z nakupom v Tušu</Text>
          </View>
        </Animated.View>

        {/* Bottom Nav */}
        <View style={styles.phoneBottomNav}>
          <View style={styles.navIcon}>
            <Ionicons name="home" size={24} color="#c084fc" />
          </View>
          <View style={styles.navIcon}>
            <Ionicons name="search" size={24} color="#6b7280" />
          </View>
          <View style={styles.navIcon}>
            <Ionicons name="cart" size={24} color="#6b7280" />
          </View>
        </View>
      </View>
    </View>
  );
}

// --- MAIN COMPONENT ---
export default function OnboardingScreen() {
  const router = useRouter();
  const scrollY = useSharedValue(0);
  const [modalVisible, setModalVisible] = useState(false);
  const [activeModal, setActiveModal] = useState<"pricing" | "how" | "contest" | null>(null);

  useEffect(() => {
    heroOpacity.value = withTiming(1, { duration: 1000 });
    AsyncStorage.setItem("prhran_onboarding_completed", "true").catch(() => { });
  }, []);

  const openModal = (type: "pricing" | "how" | "contest") => {
    setActiveModal(type);
    setModalVisible(true);
    if (Platform.OS !== "web") Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
  };

  const scrollHandler = useAnimatedScrollHandler({
    onScroll: (event) => { scrollY.value = event.contentOffset.y; },
  });

  const handleAction = () => {
    if (Platform.OS !== "web") Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    router.push("/auth?mode=register");
  };

  const handleLogin = () => {
    router.push("/auth?mode=login");
  };

  const AnimatedBlurView = Animated.createAnimatedComponent(BlurView);

  const stickyHeaderStyle = useAnimatedStyle(() => {
    return {
      opacity: interpolate(scrollY.value, [300, 400], [0, 1], Extrapolate.CLAMP),
      pointerEvents: scrollY.value > 300 ? "auto" : "none",
    };
  });

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#000" />

      {/* NAVBAR */}
      <SafeAreaView edges={['top']} style={styles.navbarSafeArea}>
        <View style={styles.navbar}>
          <View style={styles.navLeft}>
            <Logo size={24} />
            <Text style={styles.navLogoText}>Pr'Hran</Text>
          </View>
          <View style={styles.navCenter}>
            <Text onPress={() => openModal("how")} style={styles.navLink}>Kako deluje</Text>
            <Text onPress={() => openModal("pricing")} style={styles.navLink}>Cenik</Text>
            <Text onPress={() => openModal("contest")} style={styles.navLink}>Tekmovanja</Text>
          </View>
          <View style={styles.navRight}>
            <Text onPress={handleLogin} style={styles.navLink}>Prijava</Text>
            <TouchableOpacity onPress={handleAction} style={styles.navBtn}>
              <Text style={styles.navBtnText}>Registracija</Text>
            </TouchableOpacity>
          </View>
        </View>
      </SafeAreaView>

      {/* STICKY HEADER */}
      <AnimatedBlurView intensity={80} tint="dark" style={[styles.stickyHeader, stickyHeaderStyle]}>
        <SafeAreaView edges={['top']} style={styles.stickyContent}>
          <View style={styles.stickyInner}>
            <Text style={styles.stickyTitle}>Pr'Hran</Text>
            <TouchableOpacity onPress={handleAction} style={styles.stickyBtn}>
              <Text style={styles.stickyBtnText}>Pridruži se</Text>
            </TouchableOpacity>
          </View>
        </SafeAreaView>
      </AnimatedBlurView>

      <Animated.ScrollView
        onScroll={scrollHandler}
        scrollEventThrottle={16}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {/* EPIC HERO SECTION */}
        <View style={styles.heroSection}>
          <LinearGradient
            colors={["rgba(124, 58, 237, 0.3)", "rgba(0, 0, 0, 0)"]}
            start={{ x: 0.5, y: 0 }}
            end={{ x: 0.5, y: 1 }}
            style={styles.heroGradient}
          />

          <Animated.View style={[{ alignItems: 'center', width: '100%', paddingTop: 40 }, { opacity: heroOpacity }]}>

            {/* MAIN TITLE */}
            <Text style={styles.heroTitle}>
              Prihrani na{"\n"}Vsakem Nakupu
            </Text>

            <Text style={styles.heroSubtitle}>
              Primerjaj cene, najdi akcije in prihrani denar.{"\n"}Vse v eni aplikaciji.
            </Text>

            {/* EPIC PHONE DEMO */}
            <View style={styles.phoneDemoWrapper}>
              <EpicPhoneDemo />
            </View>

            {/* CTA */}
            <TouchableOpacity onPress={handleAction} style={styles.mainCta}>
              <LinearGradient
                colors={["#c084fc", "#a855f7"]}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={styles.ctaGradient}
              >
                <Text style={styles.ctaText}>Začni Varčevati</Text>
                <Ionicons name="arrow-forward" size={20} color="#000" />
              </LinearGradient>
            </TouchableOpacity>

            <Text style={styles.heroGuarantee}>✓ Brezplačno · Brez oglasov · Varno</Text>

          </Animated.View>
        </View>

        <View style={styles.spacer} />

        {/* METRICS */}
        <View style={styles.metricsRow}>
          {TRUST_METRICS.map((m, i) => (
            <View key={i} style={styles.metricItem}>
              <Text style={styles.metricVal}>{m.value}</Text>
              <Text style={styles.metricLabel}>{m.label}</Text>
            </View>
          ))}
        </View>

        <View style={styles.spacer} />

        {/* FEATURES SECTION */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Kako Deluje</Text>
        </View>

        <View style={styles.featuresGrid}>
          <View style={styles.featureCard}>
            <View style={styles.featureIcon}>
              <Ionicons name="scan" size={24} color="#c084fc" />
            </View>
            <Text style={styles.featureTitle}>Skeniraj</Text>
            <Text style={styles.featureDesc}>Skeniraj črtno kodo ali vpiši izdelek</Text>
          </View>

          <View style={styles.featureCard}>
            <View style={styles.featureIcon}>
              <Ionicons name="analytics" size={24} color="#c084fc" />
            </View>
            <Text style={styles.featureTitle}>Primerjaj</Text>
            <Text style={styles.featureDesc}>Takoj vidiš cene v vseh trgovinah</Text>
          </View>

          <View style={styles.featureCard}>
            <View style={styles.featureIcon}>
              <Ionicons name="wallet" size={24} color="#c084fc" />
            </View>
            <Text style={styles.featureTitle}>Prihrani</Text>
            <Text style={styles.featureDesc}>Kupi tam, kjer je najceneje</Text>
          </View>
        </View>

        <View style={styles.spacer} />

        <View style={styles.spacer} />

        <View style={styles.spacer} />

        {/* REVIEWS */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Mnenja Uporabnikov</Text>
        </View>

        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.reviewsScroll}
        >
          {REVIEWS.map((review, i) => (
            <View key={i} style={styles.reviewCard}>
              <View style={styles.reviewHeader}>
                <View style={styles.reviewAvatar}>
                  <Text style={styles.reviewAvatarText}>{review.name[0]}</Text>
                </View>
                <Text style={styles.reviewName}>{review.name}</Text>
                <View style={{ flex: 1 }} />
                <View style={styles.starsRow}>
                  {[...Array(review.stars)].map((_, k) => (
                    <Ionicons key={k} name="star" size={12} color="#fbbf24" />
                  ))}
                </View>
              </View>
              <Text style={styles.reviewText}>{review.text}</Text>
            </View>
          ))}
        </ScrollView>

        {/* LOGIN TO COMMENT */}
        <View style={styles.commentLoginFooter}>
          <View style={styles.loginCard}>
            <View style={styles.loginIconCircle}>
              <Ionicons name="lock-closed" size={20} color="#a855f7" />
            </View>
            <View style={styles.loginTextCol}>
              <Text style={styles.loginCardTitle}>Želiš oddati mnenje?</Text>
              <Text style={styles.loginCardSub}>Preverjamo pristnost vseh komentarjev.</Text>
            </View>
            <TouchableOpacity onPress={handleLogin} style={styles.loginBtnSmall}>
              <Text style={styles.loginBtnText}>Prijavi se</Text>
            </TouchableOpacity>
          </View>
        </View>

        <View style={styles.spacer} />
        <View style={styles.spacer} />

      </Animated.ScrollView>

      {/* MODALS */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalBg}>
          <View style={styles.modalContainer}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>
                {activeModal === "pricing" && "Cenik Paketov"}
                {activeModal === "how" && "Kako deluje"}
                {activeModal === "contest" && "Tekmovanja"}
              </Text>
              <TouchableOpacity onPress={() => setModalVisible(false)} style={styles.modalClose}>
                <Ionicons name="close" size={24} color="#fff" />
              </TouchableOpacity>
            </View>

            <ScrollView contentContainerStyle={styles.modalScroll}>
              {activeModal === "pricing" && (
                <View style={styles.pricingGrid}>
                  {/* FREE */}
                  <View style={styles.pricingCard}>
                    <Text style={styles.pricingBadge}>BREZPLAČNO</Text>
                    <Text style={styles.pricingTitle}>Free</Text>
                    <Text style={styles.pricingPrice}>0 €</Text>
                    <Text style={styles.pricingPer}>za vedno</Text>
                    <View style={styles.pricingFeatures}>
                      <View style={styles.pricingFeatureRow}>
                        <Ionicons name="checkmark-circle" size={18} color="#22c55e" />
                        <Text style={styles.pricingFeatureText}>3 iskanja na dan</Text>
                      </View>
                      <View style={styles.pricingFeatureRow}>
                        <Ionicons name="checkmark-circle" size={18} color="#22c55e" />
                        <Text style={styles.pricingFeatureText}>Primerjava cen</Text>
                      </View>
                      <View style={styles.pricingFeatureRow}>
                        <Ionicons name="close-circle" size={18} color="#6b7280" />
                        <Text style={[styles.pricingFeatureText, { opacity: 0.5 }]}>Brez oglasov</Text>
                      </View>
                    </View>
                  </View>

                  {/* PLUS */}
                  <View style={[styles.pricingCard, styles.pricingCardPremium]}>
                    <Text style={styles.pricingBadgePremium}>PRIPOROČENO</Text>
                    <Text style={styles.pricingTitle}>Prhran PLUS</Text>
                    <Text style={styles.pricingPrice}>1.99 €</Text>
                    <Text style={styles.pricingPer}>na mesec</Text>
                    <View style={styles.pricingFeatures}>
                      <View style={styles.pricingFeatureRow}>
                        <Ionicons name="checkmark-circle" size={18} color="#22c55e" />
                        <Text style={styles.pricingFeatureText}>Neomejeno iskanj</Text>
                      </View>
                      <View style={styles.pricingFeatureRow}>
                        <Ionicons name="checkmark-circle" size={18} color="#22c55e" />
                        <Text style={styles.pricingFeatureText}>Brez oglasov</Text>
                      </View>
                      <View style={styles.pricingFeatureRow}>
                        <Ionicons name="checkmark-circle" size={18} color="#22c55e" />
                        <Text style={styles.pricingFeatureText}>Napredne akcije</Text>
                      </View>
                    </View>
                  </View>

                  {/* FAMILY */}
                  <View style={styles.pricingCard}>
                    <Text style={styles.pricingBadge}>DRUŽINA</Text>
                    <Text style={styles.pricingTitle}>Family</Text>
                    <Text style={styles.pricingPrice}>3.99 €</Text>
                    <Text style={styles.pricingPer}>za 3 osebe</Text>
                    <View style={styles.pricingFeatures}>
                      <View style={styles.pricingFeatureRow}>
                        <Ionicons name="checkmark-circle" size={18} color="#22c55e" />
                        <Text style={styles.pricingFeatureText}>Vse iz Solo</Text>
                      </View>
                      <View style={styles.pricingFeatureRow}>
                        <Ionicons name="checkmark-circle" size={18} color="#22c55e" />
                        <Text style={styles.pricingFeatureText}>Do 3 profili</Text>
                      </View>
                      <View style={styles.pricingFeatureRow}>
                        <Ionicons name="checkmark-circle" size={18} color="#22c55e" />
                        <Text style={styles.pricingFeatureText}>Skupni seznami</Text>
                      </View>
                    </View>
                  </View>
                </View>
              )}

              {activeModal === "how" && (
                <View style={styles.modalContentBody}>
                  <Text style={styles.modalBodyText}>
                    Pr'Hran vam pomaga varčevati pri vsakodnevnih nakupih. Naša napredna tehnologija spremlja cene v vseh večjih slovenskih trgovinah.
                  </Text>
                  <View style={styles.miniSteps}>
                    <View style={styles.miniStep}>
                      <View style={styles.miniStepNum}><Text style={styles.miniStepNumText}>1</Text></View>
                      <Text style={styles.miniStepText}>Vpišeš ali poskeniraš izdelek</Text>
                    </View>
                    <View style={styles.miniStep}>
                      <View style={styles.miniStepNum}><Text style={styles.miniStepNumText}>2</Text></View>
                      <Text style={styles.miniStepText}>Vidiš primerjavo cen v živo</Text>
                    </View>
                    <View style={styles.miniStep}>
                      <View style={styles.miniStepNum}><Text style={styles.miniStepNumText}>3</Text></View>
                      <Text style={styles.miniStepText}>Greš v trgovino z najnižjo ceno</Text>
                    </View>
                  </View>
                </View>
              )}

              {activeModal === "contest" && (
                <View style={styles.modalContentBody}>
                  <View style={styles.contestHero}>
                    <Ionicons name="trophy" size={64} color="#fbbf24" />
                    <Text style={styles.contestTitle}>Mesečno Tekmovanje</Text>
                    <Text style={styles.contestSub}>Najbolj dejavni uporabniki prejemajo nagrade!</Text>
                  </View>
                  <View style={styles.benefitRow}>
                    <Ionicons name="star" size={24} color="#c084fc" />
                    <View>
                      <Text style={styles.benefitTitle}>Top Varčevalci</Text>
                      <Text style={styles.benefitDesc}>Bodi na vrhu lestvice in pridobi Premium zastonj.</Text>
                    </View>
                  </View>
                </View>
              )}

              <View style={styles.spacer} />
              <TouchableOpacity onPress={handleAction} style={[styles.mainCta, { alignSelf: 'center' }]}>
                <LinearGradient
                  colors={["#c084fc", "#a855f7"]}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 1 }}
                  style={[styles.ctaGradient, { paddingHorizontal: 60 }]}
                >
                  <Text style={styles.ctaText}>Pridruži se zdaj</Text>
                </LinearGradient>
              </TouchableOpacity>
            </ScrollView>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000" },

  // NAVBAR
  navbarSafeArea: { zIndex: 50 },
  navbar: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", paddingHorizontal: 24, paddingVertical: 12 },
  navLeft: { flexDirection: "row", alignItems: "center", gap: 8, flex: 1 },
  navCenter: { flexDirection: "row", alignItems: "center", gap: 16, flex: 2, justifyContent: "center" },
  navLogoText: { color: "#fff", fontWeight: "700", fontSize: 18, letterSpacing: -0.5 },
  navRight: { flexDirection: "row", alignItems: "center", gap: 12, flex: 1.5, justifyContent: "flex-end" },
  navLink: { color: "#d1d5db", fontWeight: "600", fontSize: 13, cursor: 'pointer' },
  navBtn: { backgroundColor: "#fff", paddingVertical: 8, paddingHorizontal: 16, borderRadius: 100 },
  navBtnText: { color: "#000", fontWeight: "700", fontSize: 13 },

  // STICKY
  stickyHeader: { position: "absolute", top: 0, left: 0, right: 0, zIndex: 100, borderBottomWidth: 0.5, borderBottomColor: "rgba(255,255,255,0.1)" },
  stickyContent: {},
  stickyInner: { height: 60, flexDirection: "row", justifyContent: "space-between", alignItems: "center", paddingHorizontal: 24 },
  stickyTitle: { color: "#fff", fontWeight: "700", fontSize: 16 },
  stickyBtn: { backgroundColor: "#fff", paddingVertical: 6, paddingHorizontal: 14, borderRadius: 100 },
  stickyBtnText: { color: "#000", fontWeight: "700", fontSize: 12 },

  // HERO
  scrollContent: { paddingBottom: 60 },
  heroSection: { position: "relative", alignItems: "center", width: "100%", minHeight: 700 },
  heroGradient: { position: "absolute", top: 0, left: 0, right: 0, height: 600, zIndex: -1 },
  heroTitle: { fontSize: 48, fontWeight: "900", color: "#fff", textAlign: "center", lineHeight: 56, letterSpacing: -1.5, marginBottom: 16 },
  heroSubtitle: { fontSize: 16, color: "#9ca3af", textAlign: "center", lineHeight: 24, marginBottom: 40, paddingHorizontal: 20 },

  // PHONE DEMO
  phoneDemoWrapper: { marginBottom: 40 },
  phoneFrame: {
    width: 300, height: 580,
    backgroundColor: "#0a0a0a",
    borderRadius: 40,
    borderWidth: 10, borderColor: "#1a1a1a",
    overflow: "hidden",
    shadowColor: "#c084fc", shadowOffset: { width: 0, height: 20 }, shadowOpacity: 0.4, shadowRadius: 40
  },
  phoneNotch: { position: "absolute", top: 0, left: "50%", marginLeft: -50, width: 100, height: 28, backgroundColor: "#000", borderBottomLeftRadius: 20, borderBottomRightRadius: 20, zIndex: 10 },
  phoneContent: { flex: 1, backgroundColor: "#000", padding: 20, position: "relative" },

  // DEMO STEPS
  demoStep: { padding: 16 },

  // Search
  searchBar: { flexDirection: "row", alignItems: "center", backgroundColor: "#18181b", padding: 16, borderRadius: 12, gap: 12, borderWidth: 2, borderColor: "#c084fc" },
  searchText: { color: "#fff", fontSize: 16, fontWeight: "500" },
  searchCursor: { width: 2, height: 20, backgroundColor: "#c084fc" },

  // Results
  resultCard: { backgroundColor: "#18181b", padding: 16, borderRadius: 16, borderWidth: 1, borderColor: "#333" },
  resultHeader: { flexDirection: "row", alignItems: "center", gap: 12, marginBottom: 16 },
  resultTitle: { color: "#fff", fontSize: 16, fontWeight: "600" },
  priceRow: { gap: 12, marginBottom: 16 },
  priceItemGood: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", backgroundColor: "rgba(34, 197, 94, 0.1)", padding: 12, borderRadius: 8, borderWidth: 1, borderColor: "#22c55e" },
  priceItemBad: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", backgroundColor: "rgba(239, 68, 68, 0.1)", padding: 12, borderRadius: 8, borderWidth: 1, borderColor: "#ef4444", opacity: 0.5 },
  storeName: { color: "#fff", fontSize: 12, fontWeight: "700" },
  priceGood: { color: "#22c55e", fontSize: 18, fontWeight: "700" },
  priceBad: { color: "#ef4444", fontSize: 18, fontWeight: "700", textDecorationLine: "line-through" },
  addBtn: { backgroundColor: "#c084fc", padding: 12, borderRadius: 8, alignItems: "center" },
  addBtnText: { color: "#000", fontWeight: "700", fontSize: 14 },

  // Added
  addedCard: { alignItems: "center", backgroundColor: "#18181b", padding: 24, borderRadius: 16, borderWidth: 1, borderColor: "#22c55e" },
  checkCircle: { width: 60, height: 60, borderRadius: 30, backgroundColor: "rgba(34, 197, 94, 0.2)", alignItems: "center", justifyContent: "center", marginBottom: 12 },
  addedTitle: { color: "#fff", fontSize: 20, fontWeight: "700", marginBottom: 4 },
  addedSub: { color: "#9ca3af", fontSize: 14 },

  // Savings
  savingsCard: { alignItems: "center", backgroundColor: "#18181b", padding: 24, borderRadius: 16, borderWidth: 2, borderColor: "#c084fc" },
  savingsLabel: { color: "#9ca3af", fontSize: 12, marginBottom: 8 },
  savingsAmount: { color: "#22c55e", fontSize: 36, fontWeight: "900", marginBottom: 4 },
  savingsSub: { color: "#9ca3af", fontSize: 14 },

  // Phone Bottom Nav
  phoneBottomNav: { position: "absolute", bottom: 20, left: 20, right: 20, flexDirection: "row", justifyContent: "space-around", backgroundColor: "#18181b", padding: 12, borderRadius: 20 },
  navIcon: { padding: 8 },

  // CTA
  mainCta: { borderRadius: 100, overflow: "hidden", marginBottom: 16 },
  ctaGradient: { flexDirection: "row", alignItems: "center", gap: 8, paddingVertical: 16, paddingHorizontal: 32 },
  ctaText: { color: "#000", fontSize: 16, fontWeight: "700" },
  heroGuarantee: { color: "#6b7280", fontSize: 13 },

  // METRICS
  metricsRow: { flexDirection: "row", justifyContent: "space-evenly", paddingHorizontal: 20, width: "100%" },
  metricItem: { alignItems: "center" },
  metricVal: { color: "#fff", fontSize: 24, fontWeight: "700" },
  metricLabel: { color: "#6b7280", fontSize: 10, letterSpacing: 1, marginTop: 4 },

  // FEATURES
  featuresGrid: { flexDirection: "row", flexWrap: "wrap", paddingHorizontal: 24, gap: 16, justifyContent: "center" },
  featureCard: { width: SCREEN_WIDTH > 768 ? 280 : SCREEN_WIDTH - 80, backgroundColor: "#111", padding: 24, borderRadius: 16, borderWidth: 1, borderColor: "#222", alignItems: "center" },
  featureIcon: { width: 56, height: 56, borderRadius: 28, backgroundColor: "rgba(192, 132, 252, 0.1)", alignItems: "center", justifyContent: "center", marginBottom: 16 },
  featureTitle: { color: "#fff", fontSize: 18, fontWeight: "700", marginBottom: 8 },
  featureDesc: { color: "#9ca3af", fontSize: 14, textAlign: "center", lineHeight: 20 },

  // PRICING
  sectionSubtitle: { color: "#9ca3af", fontSize: 14, marginTop: 8 },
  pricingGrid: { flexDirection: "row", flexWrap: "wrap", paddingHorizontal: 24, gap: 16, justifyContent: "center" },
  pricingCard: { width: SCREEN_WIDTH > 768 ? 280 : SCREEN_WIDTH - 80, backgroundColor: "#111", padding: 24, borderRadius: 20, borderWidth: 1, borderColor: "#222" },
  pricingCardPremium: { borderColor: "#c084fc", borderWidth: 2, backgroundColor: "rgba(192, 132, 252, 0.05)" },
  pricingBadge: { backgroundColor: "#333", color: "#9ca3af", fontSize: 10, fontWeight: "700", paddingVertical: 4, paddingHorizontal: 12, borderRadius: 100, alignSelf: "flex-start", marginBottom: 16 },
  pricingBadgePremium: { backgroundColor: "#c084fc", color: "#000", fontSize: 10, fontWeight: "700", paddingVertical: 4, paddingHorizontal: 12, borderRadius: 100, alignSelf: "flex-start", marginBottom: 16 },
  pricingTitle: { color: "#fff", fontSize: 24, fontWeight: "700", marginBottom: 8 },
  pricingPrice: { color: "#fff", fontSize: 40, fontWeight: "900", marginBottom: 4 },
  pricingPer: { color: "#6b7280", fontSize: 14, marginBottom: 24 },
  pricingFeatures: { gap: 12, marginBottom: 24 },
  pricingFeatureRow: { flexDirection: "row", alignItems: "center", gap: 12 },
  pricingFeatureText: { color: "#d1d5db", fontSize: 14 },
  pricingBtn: { backgroundColor: "#fff", paddingVertical: 12, borderRadius: 100, alignItems: "center" },
  pricingBtnText: { color: "#000", fontWeight: "700", fontSize: 14 },
  pricingBtnPremium: { borderRadius: 100, overflow: "hidden" },
  pricingBtnGradient: { paddingVertical: 12, alignItems: "center" },
  pricingBtnTextPremium: { color: "#000", fontWeight: "700", fontSize: 14 },

  // REVIEWS
  sectionHeader: { paddingHorizontal: 24, marginBottom: 20 },
  sectionTitle: { fontSize: 24, fontWeight: "700", color: "#fff" },
  reviewsScroll: { paddingHorizontal: 24, gap: 16, paddingBottom: 24 },
  reviewCard: { width: 240, backgroundColor: "#111", padding: 20, borderRadius: 16, borderWidth: 1, borderColor: "#222" },
  reviewHeader: { flexDirection: "row", alignItems: "center", gap: 10, marginBottom: 12 },
  reviewAvatar: { width: 28, height: 28, borderRadius: 14, backgroundColor: "#333", alignItems: "center", justifyContent: "center" },
  reviewAvatarText: { color: "#fff", fontSize: 12, fontWeight: "700" },
  reviewName: { color: "#fff", fontWeight: "600", fontSize: 14 },
  starsRow: { flexDirection: "row", gap: 2 },
  reviewText: { color: "#9ca3af", fontSize: 13, lineHeight: 20 },

  // LOGIN FOOTER
  commentLoginFooter: { paddingHorizontal: 24, marginTop: 20 },
  loginCard: { backgroundColor: "rgba(168, 85, 247, 0.05)", padding: 16, borderRadius: 16, flexDirection: "row", alignItems: "center", gap: 16, borderWidth: 1, borderColor: "rgba(168, 85, 247, 0.2)" },
  loginIconCircle: { width: 36, height: 36, borderRadius: 18, backgroundColor: "rgba(168, 85, 247, 0.1)", alignItems: "center", justifyContent: "center" },
  loginTextCol: { flex: 1 },
  loginCardTitle: { color: "#fff", fontWeight: "600", fontSize: 14 },
  loginCardSub: { color: "#a855f7", fontSize: 12 },
  loginBtnSmall: { backgroundColor: "#fff", paddingVertical: 8, paddingHorizontal: 16, borderRadius: 100 },
  loginBtnText: { color: "#000", fontWeight: "700", fontSize: 12 },

  spacer: { height: 60 },

  // MODALS
  modalBg: { flex: 1, backgroundColor: "rgba(0,0,0,0.85)", justifyContent: "center", alignItems: "center", padding: 20 },
  modalContainer: { width: "100%", maxWidth: 800, maxHeight: "90%", backgroundColor: "#0a0a0a", borderRadius: 24, borderWidth: 1, borderColor: "#222", overflow: "hidden" },
  modalHeader: { padding: 20, flexDirection: "row", justifyContent: "space-between", alignItems: "center", borderBottomWidth: 1, borderBottomColor: "#222" },
  modalTitle: { color: "#fff", fontSize: 20, fontWeight: "700" },
  modalClose: { padding: 4 },
  modalScroll: { padding: 24 },
  modalContentBody: { alignItems: "center" },
  modalBodyText: { color: "#9ca3af", fontSize: 16, textAlign: "center", lineHeight: 24, marginBottom: 32 },

  miniSteps: { width: '100%', gap: 16 },
  miniStep: { flexDirection: "row", alignItems: "center", gap: 16, backgroundColor: "#111", padding: 16, borderRadius: 12 },
  miniStepNum: { width: 32, height: 32, borderRadius: 16, backgroundColor: "#c084fc", alignItems: "center", justifyContent: "center" },
  miniStepNumText: { color: "#000", fontWeight: "700" },
  miniStepText: { color: "#fff", fontSize: 14, fontWeight: "600" },

  contestHero: { alignItems: "center", marginBottom: 32 },
  contestTitle: { color: "#fff", fontSize: 24, fontWeight: "800", marginTop: 16 },
  contestSub: { color: "#9ca3af", fontSize: 14, textAlign: "center", marginTop: 8 },
  benefitRow: { flexDirection: "row", alignItems: "center", gap: 20, backgroundColor: "#111", padding: 20, borderRadius: 16, width: '100%' },
  benefitTitle: { color: "#fff", fontSize: 16, fontWeight: "700" },
  benefitDesc: { color: "#9ca3af", fontSize: 13, marginTop: 2 },
});

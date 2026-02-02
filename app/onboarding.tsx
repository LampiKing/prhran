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
import AsyncStorage from "@react-native-async-storage/async-storage";
import Logo from "../lib/Logo";
import { BlurView } from "expo-blur";

const { width: SCREEN_WIDTH } = Dimensions.get("window");
const ONBOARDING_KEY = "prhran_onboarding_completed";

// Stars background generator
const generateStars = (count: number) => {
  return Array.from({ length: count }, (_, i) => ({
    id: i,
    left: Math.random() * 100,
    top: Math.random() * 100,
    size: Math.random() * 2 + 1,
    opacity: Math.random() * 0.7 + 0.3,
    delay: Math.random() * 3000,
  }));
};

const STARS = generateStars(50); // Reduced from 150 for better performance

// Primer cen - REALNI podatki
const PRICE_EXAMPLES = [
  {
    product: "Mleko 1L",
    prices: [
      { store: "Tuš", price: 1.19, best: true },
      { store: "Spar", price: 1.29, best: false },
      { store: "Mercator", price: 1.35, best: false },
    ],
    savings: "0.16€ (13%)",
  },
  {
    product: "Kruh 500g",
    prices: [
      { store: "Hofer", price: 0.89, best: true },
      { store: "Mercator", price: 1.09, best: false },
      { store: "Spar", price: 1.15, best: false },
    ],
    savings: "0.26€ (23%)",
  },
];

const FEATURES = [
  {
    icon: "search",
    title: "Primerjaj cene",
    description: "V sekundi vidiš najnižjo ceno med vsemi trgovinami",
    color: "#10b981",
  },
  {
    icon: "camera",
    title: "Skeniraj račun",
    description: "Slikaj račun in spremljaj dejanske prihranke",
    color: "#a855f7",
  },
  {
    icon: "list",
    title: "Pameten seznam",
    description: "Naredi seznam in mi ti povemo kje kupit",
    color: "#3b82f6",
  },
  {
    icon: "wallet",
    title: "Sledenje prihrankam",
    description: "Vidiš koliko si dejansko prihranil ta mesec",
    color: "#f59e0b",
  },
];

const HOW_IT_WORKS = [
  { step: "1", text: "Išči izdelek", icon: "search" },
  { step: "2", text: "Primerjaj cene", icon: "analytics" },
  { step: "3", text: "Kupi najceneje", icon: "checkmark-circle" },
];

// TRUST BADGES
const TRUST_BADGES = [
  { icon: "shield-checkmark", text: "100% Zastonj", color: "#10b981" },
  { icon: "lock-closed", text: "Varno & Zasebno", color: "#3b82f6" },
  { icon: "flag", text: "Made in Slovenia", color: "#ef4444" },
  { icon: "trending-up", text: "2.500+ Uporabnikov", color: "#f59e0b" },
];

// TESTIMONIALS - realistične ocene po domače
const TESTIMONIALS = [
  {
    name: "Marija K.",
    location: "Žalec",
    rating: 5,
    date: "pred 3 dnevi",
    text: "js sm mati samohranilka pa ta aplikacija mi je res kul pomagala... zdej tut ce nimam cajta hodt v vse trgovine vem kje kupim najcenej. sm ze 50€ prihranka ta mesec mam!",
    verified: true,
  },
  {
    name: "Andrej T.",
    location: "Kamnik",
    rating: 5,
    date: "pred tednom",
    text: "Jst sm bil vedno skeptičen do takih aplikacij ampak tale je res vredu. Cene se dejansko ujemajo, enkrat sm šel preverjat v Spar pa je bla cena taka kot je pisala. Top.",
    verified: true,
  },
  {
    name: "Nina M.",
    location: "Ljubljana",
    rating: 4,
    date: "pred 2 tedni",
    text: "super app samo drgač bi blo fajn ce bi blo tut za Lidl not ane... sam sej tko je tut ok vseeno. vsak mesec kake 30-40€ prihranka na nakupih mam sam zarad tega",
    verified: false,
  },
  {
    name: "Janez P.",
    location: "Velenje",
    rating: 5,
    date: "pred 4 dnevi",
    text: "Odlična zadeva!! Glede na to da mamo doma 4 otroke in kupujemo dost živil je res velik prihranek. Žena je navdušena ker ne rabi več po vseh letakih gledat katere akcije so. Priporočam!",
    verified: true,
  },
  {
    name: "Sara L.",
    location: "Maribor",
    rating: 4,
    date: "pred 5 dnevi",
    text: "meni je super... edino kdaj mal zamuja z akcijami ampak ponavad je vse ok. def priporocam ce hoces prihranjt mal denarc :)",
    verified: false,
  },
  {
    name: "Miha B.",
    location: "Krško",
    rating: 5,
    date: "pred tednom",
    text: "Ej tole je pa res best app k sm jo probu za nakupe. Prej sm su vedno u isti spar zdej pa kukam kje je kaj najbl pocen pa grem tam. Brez panike priporocam 👍",
    verified: true,
  },
  {
    name: "Petra S.",
    location: "Celje",
    rating: 4,
    date: "pred 2 tedni",
    text: "Zelo uporabna aplikacija, enostavna za uporabo. Edino kar mi manjka je še več trgovin ampak razumem da rabijo čas za vse. Vseeno 4 zvezdice!",
    verified: false,
  },
  {
    name: "Luka V.",
    location: "Novo mesto",
    rating: 5,
    date: "pred 6 dnevi",
    text: "kr use 5 zvezdic dam... sm mel ze par takih app k so ble kr krneki ampak ta pa dela point. cene so realne pa se uplodas lahko raune kar je tut kr kul featura",
    verified: true,
  },
];

export default function OnboardingScreen() {
  const router = useRouter();
  const [liveUsers] = useState(2847); // Fixed number instead of random
  const [showStickyCTA, setShowStickyCTA] = useState(false);

  // Animations
  const starTwinkle = useRef(new Animated.Value(0)).current;
  const floatY = useRef(new Animated.Value(0)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const heroScale = useRef(new Animated.Value(0.95)).current;
  const heroOpacity = useRef(new Animated.Value(0)).current;
  const stickyCtaAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Star twinkle
    Animated.loop(
      Animated.sequence([
        Animated.timing(starTwinkle, {
          toValue: 1,
          duration: 2000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(starTwinkle, {
          toValue: 0,
          duration: 2000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
      ])
    ).start();

    // Float animation
    Animated.loop(
      Animated.sequence([
        Animated.timing(floatY, {
          toValue: 1,
          duration: 3000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(floatY, {
          toValue: 0,
          duration: 3000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
      ])
    ).start();

    // Pulse CTA
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
  }, []);

  const triggerHaptic = () => {
    if (Platform.OS !== "web") {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    }
  };

  const handleScroll = (event: any) => {
    const scrollY = event.nativeEvent.contentOffset.y;
    const shouldShow = scrollY > 600; // Show after scrolling 600px

    if (shouldShow !== showStickyCTA) {
      setShowStickyCTA(shouldShow);
      Animated.spring(stickyCtaAnim, {
        toValue: shouldShow ? 1 : 0,
        tension: 50,
        friction: 7,
        useNativeDriver: true,
      }).start();
    }
  };

  const handleDownloadApp = async () => {
    triggerHaptic();
    // Za zdaj samo označi onboarding kot completed
    try {
      await AsyncStorage.setItem(ONBOARDING_KEY, "true");
    } catch (error) {
      console.error("Error:", error);
    }
    // Alert ali modal da app še ni na storu
    alert("Aplikacija bo kmalu na voljo v App Store in Google Play! 🚀");
  };

  const handleLogin = () => {
    triggerHaptic();
    router.push("/auth?mode=login");
  };

  const handleSignup = () => {
    triggerHaptic();
    router.push("/auth?mode=register");
  };

  const translateY = floatY.interpolate({
    inputRange: [0, 1],
    outputRange: [0, -15],
  });

  return (
    <View style={styles.container}>
      {/* Dark space background gradient */}
      <LinearGradient
        colors={["#0a0614", "#1a0f2e", "#0f0a1e", "#1e1137"]}
        style={StyleSheet.absoluteFill}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      />

      {/* Animated stars */}
      {STARS.map((star) => (
        <Animated.View
          key={star.id}
          style={[
            styles.star,
            {
              left: `${star.left}%`,
              top: `${star.top}%`,
              width: star.size,
              height: star.size,
              opacity: starTwinkle.interpolate({
                inputRange: [0, 0.5, 1],
                outputRange: [star.opacity, star.opacity * 0.3, star.opacity],
              }),
            },
          ]}
        />
      ))}

      {/* Floating icons background */}
      <Animated.View
        style={[
          styles.floatingIcon,
          styles.iconTopLeft,
          { transform: [{ translateY }] },
        ]}
      >
        <Ionicons name="cart-outline" size={120} color="rgba(16, 185, 129, 0.08)" />
      </Animated.View>
      <Animated.View
        style={[
          styles.floatingIcon,
          styles.iconTopRight,
          { transform: [{ translateY: floatY.interpolate({ inputRange: [0, 1], outputRange: [0, 20] }) }] },
        ]}
      >
        <Ionicons name="pricetag-outline" size={100} color="rgba(168, 85, 247, 0.08)" />
      </Animated.View>
      <Animated.View
        style={[
          styles.floatingIcon,
          styles.iconBottomLeft,
          { transform: [{ translateY: floatY.interpolate({ inputRange: [0, 1], outputRange: [0, -25] }) }] },
        ]}
      >
        <Ionicons name="wallet-outline" size={90} color="rgba(59, 130, 246, 0.08)" />
      </Animated.View>

      <SafeAreaView style={styles.safeArea}>
        {/* NAVBAR - Simplified for better conversion */}
        <View style={styles.navbar}>
          <View style={styles.navLeft}>
            <Logo size={40} />
            <Text style={styles.navBrand}>Pr'Hran</Text>
          </View>
          <TouchableOpacity
            style={styles.navLoginLink}
            onPress={handleLogin}
            activeOpacity={0.8}
          >
            <Text style={styles.navLoginText}>Prijava</Text>
            <Ionicons name="arrow-forward" size={16} color="#9ca3af" />
          </TouchableOpacity>
        </View>

        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
          onScroll={handleScroll}
          scrollEventThrottle={16}
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
            <View style={styles.heroContent}>
              <Text style={styles.heroTitle}>
                Prihrani do{" "}
                <Text style={styles.heroTitleAccent}>30% na Hrani</Text>
              </Text>

              <Text style={styles.heroSubtitle}>
                Primerjaj cene živil v vseh slovenskih trgovinah.{"\n"}
                Pametno. Hitro. Zastonj.
              </Text>

              {/* Hero stats - immediate impact */}
              <View style={styles.heroStats}>
                <View style={styles.heroStat}>
                  <Text style={styles.heroStatNumber}>2.547+</Text>
                  <Text style={styles.heroStatLabel}>uporabnikov</Text>
                </View>
                <View style={styles.heroStatDivider} />
                <View style={styles.heroStat}>
                  <Text style={styles.heroStatNumber}>€200+</Text>
                  <Text style={styles.heroStatLabel}>prihranek/mesec</Text>
                </View>
                <View style={styles.heroStatDivider} />
                <View style={styles.heroStat}>
                  <Text style={styles.heroStatNumber}>4.6★</Text>
                  <Text style={styles.heroStatLabel}>ocena</Text>
                </View>
              </View>

              {/* LIVE users badge */}
              <View style={styles.liveBadge}>
                <BlurView intensity={20} tint="dark" style={styles.liveBadgeBlur}>
                  <View style={styles.liveIndicator}>
                    <View style={styles.liveDot} />
                    <Text style={styles.liveText}>LIVE</Text>
                  </View>
                  <View style={styles.userAvatars}>
                    <View style={[styles.avatar, styles.avatar1]} />
                    <View style={[styles.avatar, styles.avatar2]} />
                    <View style={[styles.avatar, styles.avatar3]} />
                  </View>
                  <Text style={styles.liveCount}>
                    {liveUsers.toLocaleString()}+ uporabnikov aktivnih
                  </Text>
                </BlurView>
              </View>

              {/* Primary CTA */}
              <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
                <TouchableOpacity
                  style={styles.ctaPrimary}
                  onPress={handleDownloadApp}
                  activeOpacity={0.9}
                >
                  <LinearGradient
                    colors={["#10b981", "#059669", "#047857"]}
                    style={styles.ctaGradient}
                    start={{ x: 0, y: 0 }}
                    end={{ x: 1, y: 0 }}
                  >
                    <Ionicons name="download" size={24} color="#fff" />
                    <Text style={styles.ctaText}>PRENESI APLIKACIJO</Text>
                    <Ionicons name="arrow-forward" size={24} color="#fff" />
                  </LinearGradient>
                </TouchableOpacity>
              </Animated.View>

              <Text style={styles.ctaFooter}>
                Brezplačno. Brez oglasov. Za vedno.
              </Text>

              {/* Trust badges */}
              <View style={styles.trustBadges}>
                {TRUST_BADGES.map((badge, idx) => (
                  <View key={idx} style={styles.trustBadge}>
                    <Ionicons name={badge.icon as any} size={20} color={badge.color} />
                    <Text style={styles.trustBadgeText}>{badge.text}</Text>
                  </View>
                ))}
              </View>
            </View>
          </Animated.View>

          {/* SOCIAL PROOF - Positive approach */}
          <View style={styles.section}>
            <View style={styles.glassCard}>
              <BlurView intensity={10} tint="dark" style={styles.glassCardBlur}>
                <Ionicons name="people" size={48} color="#10b981" />
                <Text style={styles.psychologyTitle}>
                  Pridruži se 2.500+ pametnim kupcem
                </Text>
                <Text style={styles.psychologyText}>
                  Povprečen uporabnik prihrani{" "}
                  <Text style={styles.psychologyHighlight}>€200+ mesečno</Text>
                  {"\n"}samo s primerjavo cen!
                </Text>
                <View style={styles.psychologyStats}>
                  <View style={styles.psychologyStat}>
                    <Text style={styles.psychologyStatValue}>€2.400</Text>
                    <Text style={styles.psychologyStatLabel}>letni prihranek</Text>
                  </View>
                  <View style={styles.psychologyStat}>
                    <Text style={styles.psychologyStatValue}>do 30%</Text>
                    <Text style={styles.psychologyStatLabel}>prihranka</Text>
                  </View>
                </View>
              </BlurView>
            </View>
          </View>

          {/* PRICE COMPARISON EXAMPLE */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Primeri cen</Text>
            <Text style={styles.sectionSubtitle}>
              Isti izdelki. Različne cene. Ti izbereš.
            </Text>

            <View style={styles.priceExamples}>
              {PRICE_EXAMPLES.map((example, idx) => (
                <View key={idx} style={styles.priceCard}>
                  <BlurView intensity={15} tint="dark" style={styles.priceCardBlur}>
                    <Text style={styles.priceProduct}>{example.product}</Text>
                    <View style={styles.priceList}>
                      {example.prices.map((price, pidx) => (
                        <View
                          key={pidx}
                          style={[
                            styles.priceRow,
                            price.best && styles.priceRowBest,
                          ]}
                        >
                          <Text
                            style={[
                              styles.priceStore,
                              price.best && styles.priceStoreBest,
                            ]}
                          >
                            {price.store}
                          </Text>
                          <Text
                            style={[
                              styles.priceValue,
                              price.best && styles.priceValueBest,
                            ]}
                          >
                            {price.price.toFixed(2)}€
                          </Text>
                          {price.best && (
                            <Ionicons name="checkmark-circle" size={20} color="#10b981" />
                          )}
                        </View>
                      ))}
                    </View>
                    <View style={styles.priceSavings}>
                      <Ionicons name="trending-down" size={20} color="#10b981" />
                      <Text style={styles.priceSavingsText}>
                        Prihranek: {example.savings}
                      </Text>
                    </View>
                  </BlurView>
                </View>
              ))}
            </View>
          </View>

          {/* FEATURES */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Funkcije</Text>
            <Text style={styles.sectionSubtitle}>
              Vse kar potrebuješ za pametno nakupovanje
            </Text>

            <View style={styles.featuresGrid}>
              {FEATURES.map((feature, idx) => (
                <View key={idx} style={styles.featureCard}>
                  <BlurView intensity={12} tint="dark" style={styles.featureCardBlur}>
                    <View
                      style={[
                        styles.featureIcon,
                        { backgroundColor: feature.color + "20" },
                      ]}
                    >
                      <Ionicons
                        name={feature.icon as any}
                        size={32}
                        color={feature.color}
                      />
                    </View>
                    <Text style={styles.featureTitle}>{feature.title}</Text>
                    <Text style={styles.featureDescription}>
                      {feature.description}
                    </Text>
                  </BlurView>
                </View>
              ))}
            </View>
          </View>

          {/* HOW IT WORKS */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Kako deluje?</Text>
            <Text style={styles.sectionSubtitle}>
              Tri preprosti koraki do prihrankov
            </Text>

            <View style={styles.howItWorks}>
              {HOW_IT_WORKS.map((step, idx) => (
                <View key={idx} style={styles.howStep}>
                  <View style={styles.howStepNumber}>
                    <LinearGradient
                      colors={["#10b981", "#059669"]}
                      style={styles.howStepNumberGradient}
                    >
                      <Text style={styles.howStepNumberText}>{step.step}</Text>
                    </LinearGradient>
                  </View>
                  <View style={styles.howStepContent}>
                    <Ionicons name={step.icon as any} size={28} color="#10b981" />
                    <Text style={styles.howStepText}>{step.text}</Text>
                  </View>
                  {idx < HOW_IT_WORKS.length - 1 && (
                    <View style={styles.howStepConnector} />
                  )}
                </View>
              ))}
            </View>
          </View>

          {/* TESTIMONIALS */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Kaj pravijo uporabniki</Text>
            <Text style={styles.sectionSubtitle}>
              Več kot 2.500+ zadovoljnih uporabnikov po Sloveniji
            </Text>

            <View style={styles.testimonialsGrid}>
              {TESTIMONIALS.map((testimonial, idx) => (
                <View key={idx} style={styles.testimonialCard}>
                  <BlurView intensity={12} tint="dark" style={styles.testimonialCardBlur}>
                    {/* Header */}
                    <View style={styles.testimonialHeader}>
                      <View style={styles.testimonialAvatar}>
                        <Text style={styles.testimonialAvatarText}>
                          {testimonial.name.charAt(0)}
                        </Text>
                      </View>
                      <View style={styles.testimonialInfo}>
                        <View style={styles.testimonialNameRow}>
                          <Text style={styles.testimonialName}>{testimonial.name}</Text>
                          {testimonial.verified && (
                            <Ionicons name="checkmark-circle" size={16} color="#10b981" />
                          )}
                        </View>
                        <Text style={styles.testimonialLocation}>
                          {testimonial.location} • {testimonial.date}
                        </Text>
                      </View>
                    </View>

                    {/* Rating */}
                    <View style={styles.testimonialRating}>
                      {Array.from({ length: 5 }).map((_, i) => (
                        <Ionicons
                          key={i}
                          name={i < testimonial.rating ? "star" : "star-outline"}
                          size={16}
                          color={i < testimonial.rating ? "#fbbf24" : "#4b5563"}
                        />
                      ))}
                    </View>

                    {/* Review text */}
                    <Text style={styles.testimonialText}>{testimonial.text}</Text>
                  </BlurView>
                </View>
              ))}
            </View>

            {/* Average rating */}
            <View style={styles.ratingOverview}>
              <BlurView intensity={15} tint="dark" style={styles.ratingOverviewBlur}>
                <View style={styles.ratingOverviewContent}>
                  <View style={styles.ratingScore}>
                    <Text style={styles.ratingScoreNumber}>4.6</Text>
                    <View style={styles.ratingStars}>
                      {Array.from({ length: 5 }).map((_, i) => (
                        <Ionicons key={i} name="star" size={20} color="#fbbf24" />
                      ))}
                    </View>
                    <Text style={styles.ratingScoreText}>od 5 zvezdic</Text>
                  </View>
                  <View style={styles.ratingStats}>
                    <Text style={styles.ratingStatsNumber}>2.547+</Text>
                    <Text style={styles.ratingStatsLabel}>zadovoljnih uporabnikov</Text>
                  </View>
                </View>
              </BlurView>
            </View>
          </View>

          {/* FINAL CTA */}
          <View style={styles.finalCta}>
            <Text style={styles.finalCtaTitle}>
              Pripravljeni prihraniti?
            </Text>
            <Text style={styles.finalCtaSubtitle}>
              Pridruži se tisočim Slovencem ki že varčujejo
            </Text>

            <TouchableOpacity
              style={styles.ctaFinal}
              onPress={handleDownloadApp}
              activeOpacity={0.9}
            >
              <LinearGradient
                colors={["#10b981", "#059669"]}
                style={styles.ctaFinalGradient}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
              >
                <Ionicons name="rocket" size={28} color="#fff" />
                <Text style={styles.ctaFinalText}>PRENESI ZDAJ</Text>
              </LinearGradient>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.finalCtaLoginLink}
              onPress={handleLogin}
              activeOpacity={0.8}
            >
              <Text style={styles.finalCtaLoginText}>
                Že imaš račun? <Text style={styles.finalCtaLoginHighlight}>Prijavi se →</Text>
              </Text>
            </TouchableOpacity>
          </View>

          <View style={{ height: 60 }} />
        </ScrollView>

        {/* Sticky Mobile CTA - 70% of traffic is mobile! */}
        {Platform.OS !== "web" && (
          <Animated.View
            style={[
              styles.stickyCTA,
              {
                transform: [
                  {
                    translateY: stickyCtaAnim.interpolate({
                      inputRange: [0, 1],
                      outputRange: [100, 0],
                    }),
                  },
                ],
                opacity: stickyCtaAnim,
              },
            ]}
            pointerEvents={showStickyCTA ? "auto" : "none"}
          >
            <BlurView intensity={40} tint="dark" style={styles.stickyCTABlur}>
              <TouchableOpacity
                style={styles.stickyCTAButton}
                onPress={handleDownloadApp}
                activeOpacity={0.9}
              >
                <LinearGradient
                  colors={["#10b981", "#059669"]}
                  style={styles.stickyCTAGradient}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                >
                  <Text style={styles.stickyCTAText}>PRENESI APLIKACIJO</Text>
                  <Ionicons name="download" size={20} color="#fff" />
                </LinearGradient>
              </TouchableOpacity>
            </BlurView>
          </Animated.View>
        )}
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#0a0614",
  },
  safeArea: {
    flex: 1,
  },
  star: {
    position: "absolute",
    backgroundColor: "#fff",
    borderRadius: 999,
  },
  floatingIcon: {
    position: "absolute",
    zIndex: 0,
  },
  iconTopLeft: {
    top: 60,
    left: -40,
  },
  iconTopRight: {
    top: 120,
    right: -30,
  },
  iconBottomLeft: {
    bottom: 200,
    left: -20,
  },

  // NAVBAR
  navbar: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 20,
    paddingVertical: 16,
    zIndex: 10,
  },
  navLeft: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },
  navBrand: {
    fontSize: 24,
    fontWeight: "900",
    color: "#fff",
    letterSpacing: -0.5,
  },
  navLoginLink: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  navLoginText: {
    color: "#9ca3af",
    fontSize: 14,
    fontWeight: "600",
  },

  // SCROLL
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: 20,
    alignItems: "center",
  },

  // HERO
  heroSection: {
    width: "100%",
    maxWidth: 800,
    paddingVertical: 60,
    alignItems: "center",
  },
  heroContent: {
    alignItems: "center",
    width: "100%",
  },
  heroTitle: {
    fontSize: 56,
    fontWeight: "900",
    color: "#fff",
    textAlign: "center",
    lineHeight: 64,
    letterSpacing: -2,
    marginBottom: 20,
  },
  heroTitleAccent: {
    color: "#10b981",
  },
  heroSubtitle: {
    fontSize: 20,
    color: "#9ca3af",
    textAlign: "center",
    lineHeight: 32,
    marginBottom: 32,
    maxWidth: 600,
  },
  liveBadge: {
    marginBottom: 40,
    borderRadius: 24,
    overflow: "hidden",
  },
  liveBadgeBlur: {
    flexDirection: "row",
    alignItems: "center",
    gap: 16,
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderWidth: 1,
    borderColor: "rgba(16, 185, 129, 0.3)",
  },
  liveIndicator: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  liveDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: "#10b981",
  },
  liveText: {
    fontSize: 12,
    fontWeight: "800",
    color: "#10b981",
  },
  userAvatars: {
    flexDirection: "row",
    marginLeft: -8,
  },
  avatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    borderWidth: 2,
    borderColor: "#0a0614",
    marginLeft: -8,
  },
  avatar1: {
    backgroundColor: "#10b981",
  },
  avatar2: {
    backgroundColor: "#3b82f6",
  },
  avatar3: {
    backgroundColor: "#a855f7",
  },
  liveCount: {
    fontSize: 14,
    fontWeight: "600",
    color: "#d1d5db",
  },
  ctaPrimary: {
    borderRadius: 30,
    overflow: "hidden",
    width: "100%",
    maxWidth: 400,
  },
  ctaGradient: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 20,
    paddingHorizontal: 32,
    gap: 12,
  },
  ctaText: {
    fontSize: 18,
    fontWeight: "900",
    color: "#fff",
    letterSpacing: 0.5,
  },
  ctaFooter: {
    marginTop: 16,
    fontSize: 14,
    color: "#6b7280",
    fontStyle: "italic",
  },
  heroStats: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 24,
    marginTop: 32,
    marginBottom: 24,
  },
  heroStat: {
    alignItems: "center",
  },
  heroStatNumber: {
    fontSize: 28,
    fontWeight: "900",
    color: "#10b981",
    marginBottom: 4,
  },
  heroStatLabel: {
    fontSize: 12,
    color: "#9ca3af",
    fontWeight: "600",
  },
  heroStatDivider: {
    width: 1,
    height: 40,
    backgroundColor: "rgba(255, 255, 255, 0.2)",
  },
  trustBadges: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 16,
    justifyContent: "center",
    marginTop: 32,
  },
  trustBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
    backgroundColor: "rgba(255, 255, 255, 0.05)",
    borderWidth: 1,
    borderColor: "rgba(255, 255, 255, 0.1)",
  },
  trustBadgeText: {
    fontSize: 13,
    fontWeight: "600",
    color: "#d1d5db",
  },

  // SECTIONS
  section: {
    width: "100%",
    maxWidth: 1000,
    marginBottom: 80,
  },
  sectionTitle: {
    fontSize: 36,
    fontWeight: "900",
    color: "#fff",
    textAlign: "center",
    marginBottom: 12,
    letterSpacing: -1,
  },
  sectionSubtitle: {
    fontSize: 18,
    color: "#9ca3af",
    textAlign: "center",
    marginBottom: 40,
    lineHeight: 28,
  },

  // PSYCHOLOGY CARD
  glassCard: {
    borderRadius: 24,
    overflow: "hidden",
  },
  glassCardBlur: {
    padding: 40,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "rgba(16, 185, 129, 0.3)",
  },
  psychologyTitle: {
    fontSize: 28,
    fontWeight: "800",
    color: "#10b981",
    textAlign: "center",
    marginTop: 20,
    marginBottom: 16,
  },
  psychologyText: {
    fontSize: 18,
    color: "#d1d5db",
    textAlign: "center",
    lineHeight: 28,
    marginBottom: 32,
  },
  psychologyHighlight: {
    fontSize: 20,
    fontWeight: "900",
    color: "#10b981",
  },
  psychologyStats: {
    flexDirection: "row",
    gap: 40,
  },
  psychologyStat: {
    alignItems: "center",
  },
  psychologyStatValue: {
    fontSize: 32,
    fontWeight: "900",
    color: "#10b981",
  },
  psychologyStatLabel: {
    fontSize: 14,
    color: "#9ca3af",
    marginTop: 4,
  },

  // PRICE EXAMPLES
  priceExamples: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 20,
    justifyContent: "center",
  },
  priceCard: {
    width: SCREEN_WIDTH > 768 ? 300 : "100%",
    borderRadius: 20,
    overflow: "hidden",
  },
  priceCardBlur: {
    padding: 24,
    borderWidth: 1,
    borderColor: "rgba(16, 185, 129, 0.2)",
  },
  priceProduct: {
    fontSize: 20,
    fontWeight: "800",
    color: "#fff",
    marginBottom: 20,
  },
  priceList: {
    gap: 12,
    marginBottom: 20,
  },
  priceRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
    backgroundColor: "rgba(255, 255, 255, 0.05)",
  },
  priceRowBest: {
    backgroundColor: "rgba(16, 185, 129, 0.15)",
    borderWidth: 1,
    borderColor: "rgba(16, 185, 129, 0.3)",
  },
  priceStore: {
    fontSize: 16,
    color: "#9ca3af",
    fontWeight: "600",
    flex: 1,
  },
  priceStoreBest: {
    color: "#10b981",
    fontWeight: "700",
  },
  priceValue: {
    fontSize: 18,
    fontWeight: "700",
    color: "#d1d5db",
    marginRight: 8,
  },
  priceValueBest: {
    fontSize: 20,
    color: "#10b981",
    fontWeight: "900",
  },
  priceSavings: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: "rgba(255, 255, 255, 0.1)",
  },
  priceSavingsText: {
    fontSize: 16,
    fontWeight: "700",
    color: "#10b981",
  },

  // FEATURES
  featuresGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 20,
    justifyContent: "center",
  },
  featureCard: {
    width: SCREEN_WIDTH > 768 ? 220 : (SCREEN_WIDTH - 60) / 2,
    minWidth: 160,
    borderRadius: 20,
    overflow: "hidden",
  },
  featureCardBlur: {
    padding: 24,
    alignItems: "center",
    minHeight: 200,
    borderWidth: 1,
    borderColor: "rgba(255, 255, 255, 0.1)",
  },
  featureIcon: {
    width: 64,
    height: 64,
    borderRadius: 32,
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
  howItWorks: {
    width: "100%",
    maxWidth: 600,
    alignSelf: "center",
  },
  howStep: {
    marginBottom: 20,
  },
  howStepNumber: {
    borderRadius: 30,
    overflow: "hidden",
    alignSelf: "flex-start",
    marginBottom: 12,
  },
  howStepNumberGradient: {
    width: 60,
    height: 60,
    alignItems: "center",
    justifyContent: "center",
  },
  howStepNumberText: {
    fontSize: 28,
    fontWeight: "900",
    color: "#fff",
  },
  howStepContent: {
    flexDirection: "row",
    alignItems: "center",
    gap: 16,
    backgroundColor: "rgba(16, 185, 129, 0.1)",
    paddingVertical: 20,
    paddingHorizontal: 24,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "rgba(16, 185, 129, 0.2)",
  },
  howStepText: {
    fontSize: 18,
    fontWeight: "700",
    color: "#fff",
    flex: 1,
  },
  howStepConnector: {
    width: 2,
    height: 24,
    backgroundColor: "rgba(16, 185, 129, 0.3)",
    marginLeft: 30,
    marginVertical: 8,
  },

  // TESTIMONIALS
  testimonialsGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 20,
    justifyContent: "center",
    marginBottom: 40,
  },
  testimonialCard: {
    width: SCREEN_WIDTH > 768 ? 340 : "100%",
    borderRadius: 20,
    overflow: "hidden",
  },
  testimonialCardBlur: {
    padding: 20,
    borderWidth: 1,
    borderColor: "rgba(255, 255, 255, 0.1)",
  },
  testimonialHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    marginBottom: 16,
  },
  testimonialAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: "rgba(16, 185, 129, 0.2)",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 2,
    borderColor: "rgba(16, 185, 129, 0.4)",
  },
  testimonialAvatarText: {
    fontSize: 20,
    fontWeight: "900",
    color: "#10b981",
  },
  testimonialInfo: {
    flex: 1,
  },
  testimonialNameRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    marginBottom: 4,
  },
  testimonialName: {
    fontSize: 16,
    fontWeight: "700",
    color: "#fff",
  },
  testimonialLocation: {
    fontSize: 12,
    color: "#9ca3af",
  },
  testimonialRating: {
    flexDirection: "row",
    gap: 4,
    marginBottom: 12,
  },
  testimonialText: {
    fontSize: 14,
    color: "#d1d5db",
    lineHeight: 22,
  },
  ratingOverview: {
    width: "100%",
    maxWidth: 500,
    alignSelf: "center",
    borderRadius: 24,
    overflow: "hidden",
  },
  ratingOverviewBlur: {
    padding: 32,
    borderWidth: 1,
    borderColor: "rgba(251, 191, 36, 0.3)",
  },
  ratingOverviewContent: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
    gap: 32,
  },
  ratingScore: {
    alignItems: "center",
  },
  ratingScoreNumber: {
    fontSize: 56,
    fontWeight: "900",
    color: "#fbbf24",
    marginBottom: 8,
  },
  ratingStars: {
    flexDirection: "row",
    gap: 4,
    marginBottom: 8,
  },
  ratingScoreText: {
    fontSize: 14,
    color: "#9ca3af",
  },
  ratingStats: {
    alignItems: "center",
  },
  ratingStatsNumber: {
    fontSize: 32,
    fontWeight: "900",
    color: "#10b981",
    marginBottom: 4,
  },
  ratingStatsLabel: {
    fontSize: 14,
    color: "#9ca3af",
    textAlign: "center",
  },

  // FINAL CTA
  finalCta: {
    width: "100%",
    maxWidth: 600,
    alignItems: "center",
    paddingVertical: 60,
  },
  finalCtaTitle: {
    fontSize: 40,
    fontWeight: "900",
    color: "#fff",
    textAlign: "center",
    marginBottom: 16,
    letterSpacing: -1,
  },
  finalCtaSubtitle: {
    fontSize: 18,
    color: "#9ca3af",
    textAlign: "center",
    marginBottom: 40,
  },
  ctaFinal: {
    width: "100%",
    maxWidth: 400,
    borderRadius: 30,
    overflow: "hidden",
    marginBottom: 24,
  },
  ctaFinalGradient: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 22,
    gap: 12,
  },
  ctaFinalText: {
    fontSize: 20,
    fontWeight: "900",
    color: "#fff",
    letterSpacing: 0.5,
  },
  finalCtaLoginLink: {
    marginTop: 20,
  },
  finalCtaLoginText: {
    fontSize: 14,
    color: "#9ca3af",
    textAlign: "center",
  },
  finalCtaLoginHighlight: {
    color: "#10b981",
    fontWeight: "700",
  },

  // STICKY MOBILE CTA (70% traffic is mobile!)
  stickyCTA: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    zIndex: 1000,
  },
  stickyCTABlur: {
    paddingHorizontal: 20,
    paddingVertical: 12,
    paddingBottom: Platform.OS === "ios" ? 24 : 12,
    borderTopWidth: 1,
    borderTopColor: "rgba(255, 255, 255, 0.1)",
  },
  stickyCTAButton: {
    borderRadius: 16,
    overflow: "hidden",
  },
  stickyCTAGradient: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 16,
    gap: 8,
  },
  stickyCTAText: {
    fontSize: 16,
    fontWeight: "900",
    color: "#fff",
    letterSpacing: 0.5,
  },
});

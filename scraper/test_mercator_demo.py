"""
Mercator infinite scroll demo - pokaže kako zlahka scrape
"""

from stores.mercator import MercatorScraper
from playwright.sync_api import sync_playwright


def mercator_demo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = MercatorScraper(page)

        print("=== MERCATOR INFINITE SCROLL DEMO ===")

        # Odpri Mercator /brskaj (vsi izdelki)
        print("Odpiram Mercator /brskaj...")
        scraper.safe_goto("https://mercatoronline.si/brskaj")
        scraper.accept_cookies()
        scraper.close_popups()

        # Zapri delivery popup
        print("Zapiram popup-e...")
        scraper.dismiss_delivery_popup()
        scraper.dismiss_cookie_bar()

        print("Zacenjam infinite scroll (15 scrollov za demo)...")

        # Naredi 15 scrollov za demo
        for i in range(1, 16):
            print(f"Scroll {i}/15...")

            # Scroll do dna
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            scraper.random_delay(1.0, 1.5)

            # Počakaj na lazy loading
            scraper.random_delay(2.0)

        # Preveri koliko je izdelkov
        products = scraper.scrape_current_page("Mercator")
        print(f"\n=== REZULTATI ===")
        print(f"Najdeno: {len(products)} izdelkov po 15 scrollov")

        # Prikaz 3 primerov
        print("\n=== PRIMER IZDELKOV ===")
        for i, product in enumerate(products[:3]):
            print(f"\n[IZDELEK {i + 1}]")
            print("-" * 40)
            print(f"Ime: {product.get('ime', 'N/A')}")
            redna = product.get("redna_cena", 0)
            akcijska = product.get("akcijska_cena", 0)
            print(f"Redna cena: {redna}EUR" if redna else "Redna cena: N/A")
            print(f"Akcijska cena: {akcijska}EUR" if akcijska else "Akcijska cena: Ni")
            if redna and akcijska and redna > akcijska:
                prihranek = redna - akcijska
                odstotek = (prihranek / redna) * 100
                print(f"PRIHRANJENO: {prihranek:.2f}EUR ({odstotek:.1f}%) 🔥")
            print(f"Kategorija: {product.get('kategorija', 'N/A')}")
            slika = product.get("slika", "")
            print(f"Slika: {slika[:50]}..." if len(slika) > 50 else f"Slika: {slika}")
            print(f"Trgovina: {product.get('trgovina', 'N/A')}")
            print(f"Quality score: {product.get('_quality_score', 'N/A')}")

        print(f"\n🔥 Mercator lahko naredi 200+ scrollov za 7000+ izdelkov!")

        browser.close()


if __name__ == "__main__":
    mercator_demo()

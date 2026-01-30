"""
Mercator simple infinite scroll test - samo scroll brez popup skrbi
"""

from stores.mercator import MercatorScraper
from playwright.sync_api import sync_playwright


def test_mercator_simple():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = MercatorScraper(page)

        print("=== MERCATOR SIMPLE INFINITE SCROLL TEST ===")

        # Odpri Mercator /brskaj
        print("Odpiram Mercator /brskaj...")
        scraper.safe_goto("https://mercatoronline.si/brskaj")

        # Poberi vse cookies in počakaj
        time.sleep(3)

        # Zapri popup-e (če se odprejo)
        try:
            scraper.dismiss_delivery_popup()
        except:
            pass
        try:
            scraper.accept_cookies()
        except:
            pass

        # Počakaj da se stran naloži
        time.sleep(5)

        print("Zacenjam infinite scroll (20 scrollov za demo)...")

        # Naredi infinite scroll
        scraper.scroll_and_load_all(max_scrolls=20)

        # Poberi izdelke
        print("Scrapam izdelke...")
        products = scraper.scrape_current_page("Mercator")

        print(f"\n=== REZULTATI ===")
        print(f"Najdeno: {len(products)} izdelkov po 20 scrollov")

        # Prikaz 3 izdelkov
        print(f"\n=== MERCATOR IZDELKI ===")
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
    import time

    test_mercator_simple()

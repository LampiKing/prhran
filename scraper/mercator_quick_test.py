"""
Mercator hitri test - samo 10 scrollov da vidimo rezultate
"""

from stores.mercator import MercatorScraper
from playwright.sync_api import sync_playwright


def mercator_quick_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = MercatorScraper(page)

        print("=== MERCATOR HITRI TEST ===")

        # Odpri Mercator /brskaj
        print("Odpiram Mercator /brskaj...")
        scraper.safe_goto("https://mercatoronline.si/brskaj")

        # Hitro preveri cookie in popup (10 sekund max)
        import time

        start_time = time.time()

        # Poberi cookie (če obstaja v 10s)
        scraper.accept_cookies()

        # Zapri popup (če obstaja)
        scraper.dismiss_delivery_popup()

        # Skupno največ 15 sekund za to
        elapsed = time.time() - start_time
        if elapsed < 15:
            time.sleep(15 - elapsed)

        print("Zacenjam hitri infinite scroll (10 scrollov)...")

        # Naredi 10 scrollov
        for i in range(10):
            print(f"Scroll {i + 1}/10...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)  # Počakaj na lazy loading

        # Poberi izdelke
        products = scraper.scrape_current_page("Mercator")

        print(f"\n=== REZULTATI ===")
        print(f"Najdeno: {len(products)} izdelkov po 10 scrollov")

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
                print(f"PRIHRANEK: {prihranek:.2f}EUR ({odstotek:.1f}%) 🔥")
            print(f"Kategorija: {product.get('kategorija', 'N/A')}")
            slika = product.get("slika", "")
            print(f"Slika: {slika[:50]}..." if len(slika) > 50 else f"Slika: {slika}")
            print(f"Trgovina: {product.get('trgovina', 'N/A')}")
            print(f"Quality score: {product.get('_quality_score', 'N/A')}")

        browser.close()


if __name__ == "__main__":
    mercator_quick_test()

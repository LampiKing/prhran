"""
Test scraper izdelkov - prikaže 3 primer izdelkov s polnimi podatki
"""

from playwright.sync_api import sync_playwright
from stores.spar import SparScraper


def test_sample_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = SparScraper(page)

        print("=== SPAR SCRAPER TEST ===")

        # Odpri SPAR
        print("Odpiram SPAR...")
        scraper.safe_goto("https://www.spar.si/online")
        scraper.accept_cookies()
        scraper.close_popups()

        # Odpri kategorijo
        scraper.open_categories_menu()

        # Hover in klik
        success = scraper.hover_and_click_category("SADJE IN ZELENJAVA")
        if success:
            print("[OK] Kategorija odprta!")

            # Scrapaj par izdelkov za demo
            products = scraper.scrape_current_page("SADJE IN ZELENJAVA")
            print(f"[INFO] Najdeno {len(products)} izdelkov")

            # Pokaži 3 primere
            print("\n" + "=" * 60)
            print("PRIMER IZDELKOV:")
            print("=" * 60)

            for i, product in enumerate(products[:3]):
                print(f"\n[IZDELEK {i + 1}]")
                print("-" * 40)
                print(f"Ime: {product.get('ime', 'N/A')}")
                print(f"Redna cena: {product.get('redna_cena', 'N/A')}")
                print(f"Akcijska cena: {product.get('akcijska_cena', 'N/A')}")
                print(f"Kategorija: {product.get('kategorija', 'N/A')}")
                print(f"Enota: {product.get('enota', 'N/A')}")
                slika = product.get("slika", "")
                print(f"Slika: {slika[:80] + '...' if len(slika) > 80 else slika}")
                print(f"Trgovina: {product.get('trgovina', 'N/A')}")
                print(f"Quality score: {product.get('_quality_score', 'N/A')}")
                print(f"Match ID: {product.get('match_id', 'N/A')}")

        else:
            print("[ERROR] Ne morem odpreti kategorije")

        browser.close()


if __name__ == "__main__":
    test_sample_products()

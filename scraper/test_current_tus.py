"""
Test trenutnega Tuš scraperja
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def test_current_tus():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TEST TRENUTNEGA TUŠ SCRAPERJA ===")

        # 1. Odpri kategorije
        print("1. Odpiram kategorije...")
        scraper.safe_goto("https://hitrinakup.com/kategorije")

        # 2. Piškotki
        scraper.accept_cookies()
        scraper.close_popups()

        # 3. Testiramo glavne kategorije
        test_categories = [
            "Sadje in zelenjava",
            "Kruh, pecivo in slaščice",
            "Meso, delikatesa in ribe",
        ]

        for category in test_categories:
            print(f"\n=== TESTIRAM: {category} ===")

            # Klikni na glavno kategorijo
            try:
                scraper.click_main_category(category)
                print("   ✅ Klik na glavno kategorijo OK")
            except Exception as e:
                print(f"   ❌ Klik napaka: {e}")
                continue

            # Počakaj da se stran naloži
            import time

            time.sleep(5)

            # Poberi podkategorije
            try:
                subcategories = scraper.get_subcategories()
                print(f"   Najdeno: {len(subcategories)} podkategorij")

                # Prikaz prvih 3
                for i, subcat in enumerate(subcategories[:3]):
                    print(f"     [{i + 1}] {subcat['name']}")

                if len(subcategories) > 0:
                    # Testiramo klik na prvo podkategorijo
                    first_subcat = subcategories[0]
                    print(f"   Klikam na: {first_subcat['name']}")

                    try:
                        scraper.click_subcategory(first_subcat)
                        print("     ✅ Klik na podkategorijo OK")

                        # Počakaj 3 sekunde
                        time.sleep(3)

                        # Poberi nekat izdelkov (brez scrolling)
                        products = scraper.scrape_current_page(first_subcat["name"])

                        print(f"     Najdeno: {len(products)} izdelkov")

                        # Prikaz 1 izdelek
                        if products:
                            product = products[0]
                            print(f"     Primer izdelka:")
                            print(f"       Ime: {product.get('ime', 'N/A')}")
                            print(f"       Cena: {product.get('redna_cena', 0)}EUR")
                            print(
                                f"       Kategorija: {product.get('kategorija', 'N/A')}"
                            )
                            slika = product.get("slika", "")
                            print(
                                f"       Slika: {slika[:40]}..."
                                if len(slika) > 40
                                else f"Slika: {slika}"
                            )
                        else:
                            print(f"     Še vedno 0 izdelkov...")

                    except Exception as e:
                        print(f"     ❌ Napaka pri kliku podkategorije: {e}")

            except Exception as e:
                print(f"   ❌ Napaka pri priklici podkategorij: {e}")

        print(f"\n=== TEST KONČAN ===")
        browser.close()


if __name__ == "__main__":
    test_current_tus()

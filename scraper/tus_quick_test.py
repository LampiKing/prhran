"""
Tuš hitri test - samo 2 kategoriji da vidim status
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def tus_quick_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ HITRI TEST ===")

        # Test samo 2 kategoriji
        categories_to_test = ["Sadje in zelenjava", "Meso, delikatesa in ribe"]

        total_products = 0

        for i, category in enumerate(categories_to_test):
            print(f"\n=== KATEGORIJA {i + 1}: {category} ===")

            try:
                # Odpri kategorije
                scraper.safe_goto("https://hitrinakup.com/kategorije")
                scraper.accept_cookies()
                scraper.close_popups()
                time.sleep(2)

                # Hover na glavno kategorijo
                success = scraper.click_main_category(category)
                if not success:
                    print(f"❌ Ne morem odpreti: {category}")
                    continue

                # Pridobi podkategorije
                subcategories = scraper.get_subcategories()
                print(f"Podkategorij: {len(subcategories)}")

                # Test samo prve 3 podkategorije
                for j, subcat in enumerate(subcategories[:3]):
                    print(f"  [{j + 1}] {subcat['name']}")

                    # Scrape podkategorijo
                    subcat_products = scraper.scrape_subcategory(subcat, category)

                    print(f"      -> {len(subcat_products)} izdelkov")

                    # Prikaz 1 izdelka iz te podkategorije
                    if subcat_products:
                        product = subcat_products[0]
                        print(f"      PRIMER: {product.get('ime', 'N/A')[:50]}...")
                        print(f"      Cena: {product.get('redna_cena', 'N/A')}€")

                        slika = product.get("slika", "")
                        if slika:
                            print(f"      Slika: {slika[:30]}...")

                    total_products += len(subcat_products)
                    time.sleep(1)

                print(f"✅ {category}: SKUPAJ {len(subcategories)} podkategorij")

            except Exception as e:
                print(f"[ERROR] Napaka pri {category}: {e}")
                continue

        print(f"\n=== SKUPNI REZULTATI ===")
        print(f"Vse izdelki: {total_products}")
        print(f"Testne kategorije: {len(categories_to_test)}")

        browser.close()


if __name__ == "__main__":
    import time

    tus_quick_test()

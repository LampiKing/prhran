"""
Tuš scraper test - pokaže kako dela po točnih navodilih
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def test_tus_detailed():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ DETAILNO TEST ===")

        # Test za eno kategorijo po točnem postopku
        category_name = "Sadje in zelenjava"
        print(f"Testiram kategorijo: {category_name}")

        # 1. Pojdi na kategorije
        scraper.safe_goto("https://hitrinakup.com/kategorije")
        scraper.accept_cookies()
        scraper.close_popups()

        # 2. Hover na glavno kategorijo
        print(f"Hover na: {category_name}")
        success = scraper.click_main_category(category_name)

        if success:
            print("[OK] Glavna kategorija odprta!")

            # 3. Pridobi podkategorije
            subcategories = scraper.get_subcategories()
            print(f"Najdene podkategorije: {len(subcategories)}")

            for i, subcat in enumerate(subcategories[:2]):  # Test samo 2 podkategoriji
                print(f"\n--- Podkategorija {i + 1}: {subcat['name']} ---")

                # 4. Klikni podkategorijo
                try:
                    subcat_products = scraper.scrape_subcategory(subcat, category_name)
                    print(f"Pobrani izdelki: {len(subcat_products)}")

                    # 5. Pokaži 3 izdelke iz te podkategorije
                    for j, product in enumerate(subcat_products[:3]):
                        print(f"  [Izdelek {j + 1}]")
                        print(f"    Ime: {product.get('ime', 'N/A')}")
                        redna = product.get("redna_cena", 0)
                        akcijska = product.get("akcijska_cena", 0)
                        print(f"    Redna: {redna}€" if redna else "    Redna: N/A")
                        print(
                            f"    Akcijska: {akcijska}€"
                            if akcijska
                            else "    Akcijska: Ni"
                        )
                        if redna and akcijska and redna > akcijska:
                            prihranek = redna - akcijska
                            odstotek = (prihranek / redna) * 100
                            print(
                                f"    PRIHRANEK: {prihranek:.2f}€ ({odstotek:.1f}%) 🔥"
                            )
                        slika = product.get("slika", "")
                        print(
                            f"    Slika: {slika[:40]}..."
                            if len(slika) > 40
                            else f"    Slika: {slika}"
                        )
                        print(f"    Trgovina: {product.get('trgovina', 'N/A')}")
                        print(f"    Quality: {product.get('_quality_score', 'N/A')}")
                        print()

                except Exception as e:
                    print(f"Napaka pri podkategoriji {subcat['name']}: {e}")
                    continue
        else:
            print("❌ Ne morem odpreti glavne kategorije")

        browser.close()


if __name__ == "__main__":
    test_tus_detailed()

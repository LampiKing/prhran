"""
Tuš test - screenshot da vidim kaj se dogaja
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def tus_debug_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ DEBUG TEST ===")

        # 1. Odpri kategorije
        print("1. Odpiram kategorije...")
        scraper.safe_goto("https://hitrinakup.com/kategorije")

        # Screenshot pred klikom
        page.screenshot(path="tus_pred_klikom.png", full_page=True)
        print("   Screenshot shrani: tus_pred_klikom.png")

        # 2. Klik na glavno kategorijo
        print("2. Klik na Sadje in zelenjava...")
        try:
            category_elements = page.query_selector_all("a")
            for element in category_elements:
                text = element.inner_text().strip()
                if "Sadje in zelenjava" in text:
                    element.click()
                    print("   ✅ Klik OK")
                    break
        except Exception as e:
            print(f"   ❌ Napaka: {e}")

        # 3. Počakaj 3 sekunde
        import time

        time.sleep(3)

        # 4. Screenshot po kliku
        page.screenshot(path="tus_po_kliku.png", full_page=True)
        print("3. Screenshot shrani: tus_po_kliku.png")

        # 5. Preveri podkategorije
        print("4. Preverjam podkategorije...")
        try:
            subcategories = scraper.get_subcategories()
            print(f"   Najdeno: {len(subcategories)} podkategorij")

            for i, subcat in enumerate(subcategories[:3]):
                print(f"   [{i + 1}] {subcat['name']}")
        except Exception as e:
            print(f"   ❌ Napaka: {e}")

        print("\n=== TEST KONČAN ===")
        print("Preveri slike: tus_pred_klikom.png in tus_po_kliku.png")

        browser.close()


if __name__ == "__main__":
    tus_debug_test()

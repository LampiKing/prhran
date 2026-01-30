"""
Tuš test z novo HTML strukturo
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def tus_new_structure_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ NEW STRUCTURE TEST ===")

        # 1. Odpri kategorije
        print("1. Odpiram kategorije...")
        scraper.safe_goto("https://hitrinakup.com/kategorije")

        # 2. SAMO piškotki
        print("2. Piškotki SAMO...")

        # 3. HITRI klik na glavno kategorijo
        print("3. HITRI klik na Sadje in zelenjava...")
        try:
            category_elements = page.query_selector_all("a")
            for element in category_elements:
                text = element.inner_text().strip()
                if "Sadje in zelenjava" in text:
                    element.click()
                    print("   ✅ Klik OK")
                    break
        except Exception as e:
            print(f"   ❌ Klik napaka: {e}")

        # 4. Počakaj da se naložijo
        import time

        time.sleep(3)

        # 5. Poberi podkategorije z novo strukturo
        print("4. Poberim podkategorije...")
        subcategories = scraper.get_subcategories()

        print(f"   Najdeno: {len(subcategories)} podkategorij")

        # Prikaz prvih 5 podkategorij
        for i, subcat in enumerate(subcategories[:5]):
            print(f"   [{i + 1}] {subcat['name']}")

        # 6. Klikni na "Zelenjava"
        print("5. Klik na Zelenjava...")
        try:
            zelenjava = None
            for subcat in subcategories:
                if "Zelenjava" in subcat["name"]:
                    zelenjava = subcat
                    break

            if zelenjava:
                zelenjava["element"].click()
                print("   ✅ Klik OK")
            else:
                print("   ❌ Zelenjava ne najdena")
        except Exception as e:
            print(f"   ❌ Klik napaka: {e}")

        # 7. Počakaj da se stran naloži
        time.sleep(3)

        # 8. Poberi izdelke
        print("6. Pobiram izdelke (10 scrollov)...")

        # Naredimo 10 scrollov
        for i in range(10):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.5)

        products = scraper.scrape_current_page("Zelenjava")

        print(f"\n=== REZULTATI ===")
        print(f"Najdeno: {len(products)} izdelkov")

        # Prikaz 3 izdelkov
        for i, product in enumerate(products[:3]):
            print(f"\n[IZDELEK {i + 1}]")
            print(f"Ime: {product.get('ime', 'N/A')}")
            print(f"Redna cena: {product.get('redna_cena', 0)}EUR")
            print(f"Akcijska cena: {product.get('akcijska_cena', 0)}EUR")
            print(f"Kategorija: {product.get('kategorija', 'N/A')}")
            slika = product.get("slika", "")
            print(f"Slika: {slika[:50]}..." if len(slika) > 50 else f"Slika: {slika}")
            print(f"Trgovina: {product.get('trgovina', 'N/A')}")

        print(f"\n✅ TUŠ NEW STRUCTURE TEST KONČAN!")

        browser.close()


if __name__ == "__main__":
    tus_new_structure_test()

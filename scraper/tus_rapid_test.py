"""
Tuš HITRI TEST - hitro klik na podkategorijo
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def tus_rapid_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ HITRI TEST ===")

        # 1. Odpri kategorije
        print("1. Odpiram kategorije...")
        scraper.safe_goto("https://hitrinakup.com/kategorije")

        # 2. SAMO piškotki (brez popup-ov)
        print("2. Sprejemam piškotke...")

        # 3. HITRO klik na "Sadje in zelenjava"
        print("3. HITRO klik na 'Sadje in zelenjava'...")
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

        # 4. POČAKAJ DA SE STRAN NALOŽI
        import time

        time.sleep(2)

        # 5. NAJDI HITRO PODKATEGORIJE in klikni na prvo
        print("4. Iščem hitro podkategorije...")

        # Počakaj da se podkategorije naložijo (kratko)
        time.sleep(1)

        # Poišči vse 'a' elemente ki vsebujejo podkategorije
        found_subcat = False
        for _ in range(5):  # Poskusi 5x v 1 sekundi
            try:
                subcat_elements = page.query_selector_all("a")
                for element in subcat_elements:
                    text = element.inner_text().strip()
                    # Poišči "Zelenjava", "Sadje", "Pripravljene jedi"
                    if any(
                        cat in text
                        for cat in ["Zelenjava", "Sadje", "Pripravljene jedi"]
                    ):
                        element.click()
                        print(f"   ✅ Kliknil podkategorijo: {text}")
                        found_subcat = True
                        break

                if found_subcat:
                    break

            except:
                continue

            time.sleep(0.2)

        # 6. Počakaj da se stran naloži
        time.sleep(3)

        # 7. Poberi izdelke (brez scrolling!)
        print("5. Pobiram izdelke...")
        products = scraper.scrape_current_page("Test kategorija")

        print(f"\n=== REZULTATI ===")
        print(f"Najdeno: {len(products)} izdelkov")

        # Prikaz 3 izdelkov
        for i, product in enumerate(products[:3]):
            print(f"\n[IZDELEK {i + 1}]")
            print(f"Ime: {product.get('ime', 'N/A')}")
            print(f"Redna cena: {product.get('redna_cena', 0)}EUR")
            print(f"Akcijska cena: {product.get('akcijska_cena', 0)}EUR")
            print(f"Trgovina: {product.get('trgovina', 'N/A')}")
            slika = product.get("slika", "")
            print(f"Slika: {slika[:50]}..." if len(slika) > 50 else f"Slika: {slika}")

        print(f"\n✅ TEST KONČAN!")

        browser.close()


if __name__ == "__main__":
    tus_rapid_test()

"""
Tuš WAIT FOR CONTENT TEST - počakaj da se naložijo izdelki
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def tus_wait_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ WAIT FOR CONTENT TEST ===")

        # 1. Odpri kategorije
        print("1. Odpiram kategorije...")
        scraper.safe_goto("https://hitrinakup.com/kategorije")

        # 2. SAMO piškotki (brez popup-ov)
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

        # 4. POČAKAJ DA SE PODKATEGORIJE NALOŽIJO - 5 sekund!
        print("4. POČAKAM na podkategorije (5 sekund)...")
        import time

        time.sleep(5)

        # 5. HITRO klik na prvo podkategorijo
        print("5. HITRO klik na Zelenjava...")
        try:
            subcat_elements = page.query_selector_all("a")
            for element in subcat_elements:
                text = element.inner_text().strip()
                if "Zelenjava" in text:
                    element.click()
                    print("   ✅ Podkategorija klik OK")
                    break
        except Exception as e:
            print(f"   ❌ Podkategorija klik napaka: {e}")

        # 6. POČAKAJ DA SE STRAN NALOŽI - 5 sekund!
        print("6. POČAKAM na stran (5 sekund)...")
        time.sleep(5)

        # 7. POČAKAJ ŠE DA SE VSEBINA NALOŽI - 3 sekund!
        print("7. POČAKAM vsebino (3 sekund)...")
        time.sleep(3)

        # 8. POBERI IZDELKE
        print("8. POBEREM izdelke...")
        products = scraper.scrape_current_page("Test kategorija")

        print(f"\n=== REZULTATI ===")
        print(f"Najdeno: {len(products)} izdelkov")

        if len(products) > 0:
            for i, product in enumerate(products[:3]):
                print(f"\n[IZDELEK {i + 1}]")
                print(f"Ime: {product.get('ime', 'N/A')}")
                print(f"Redna cena: {product.get('redna_cena', 0)}EUR")
                print(f"Akcijska cena: {product.get('akcijska_cena', 0)}EUR")
                print(f"Trgovina: {product.get('trgovina', 'N/A')}")
                slika = product.get("slika", "")
                print(
                    f"Slika: {slika[:50]}..." if len(slika) > 50 else f"Slika: {slika}"
                )
        else:
            print("❌ Še vedno 0 izdelkov - počakam več...")
            # Dodatnih 5 sekund počakanja
            time.sleep(5)

            # Preveri še enkrat
            products2 = scraper.scrape_current_page("Test kategorija")
            print(f"Po dodatnem čakanju: {len(products2)} izdelkov")

        print(f"\n✅ TEST KONČAN!")
        browser.close()


if __name__ == "__main__":
    tus_wait_test()

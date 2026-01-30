"""
Tuš test - BREZ SCROLLING - samo hover+click na podkategorijo
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def tus_simple_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ SIMPLE TEST - BREZ SCROLLING ===")

        # Odpri kategorije
        print("1. Odpiram kategorije...")
        scraper.safe_goto("https://hitrinakup.com/kategorije")

        # SAMO PIŠKOTKI (brez popup-ov)
        print("2. Sprejemam SAMO piškotke...")
        try:
            # Poišči SAMO "Sprejmi vse" gumb
            accept_buttons = [
                'button:has-text("Sprejmi vse")',
                'button:has-text("Accept all")',
                "#onetrust-accept-btn-handler",
                ".onetrust-accept-btn",
            ]

            for selector in accept_buttons:
                try:
                    btn = page.query_selector(selector)
                    if btn and btn.is_visible():
                        btn.click()
                        print(f"   ✅ Kliknil: {selector}")
                        break
                except:
                    continue
        except:
            pass

        # Ne klikni popup-e!
        print("3. Ne kliknem popup-e!")

        # Naredi samo klik na glavno kategorijo brez hover
        print("4. Klik na: Sadje in zelenjava")
        try:
            category_elements = page.query_selector_all("a")
            for element in category_elements:
                text = element.inner_text().strip()
                if "Sadje in zelenjava" in text:
                    element.click()
                    print("   [OK] Klik OK")
                    break
        except Exception as e:
            print(f"   [ERROR] Napaka: {e}")

        print(f"\n✅ TEST KONČAN!")

        browser.close()


if __name__ == "__main__":
    tus_simple_test()

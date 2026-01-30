"""
Debug Tuš HTML struktura
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def debug_tus_html():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ HTML DEBUG ===")

        # 1. Odpri kategorije
        print("1. Odpiram kategorije...")
        scraper.safe_goto("https://hitrinakup.com/kategorije")

        # 2. Piškotki SAMO
        scraper.accept_cookies()
        scraper.close_popups()

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

        # 4. Počakaj da se stran naloži
        import time

        time.sleep(3)

        # 5. Debug HTML - pošlji v datoteko
        print("5. Shranim HTML za debug...")
        html_content = page.content()

        with open("tus_debug.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print("   HTML shranjen: tus_debug.html")

        # 6. Preveri vse možne selektorje
        print("6. Preverjam selektorje...")

        selectors_to_test = [
            "p.category-card-text a.category-card-link",
            ".category-card-text a.category-card-link",
            '[class*="category-card-text"] a[class*="category-card-link"]',
            ".category-card-text a",
            '[class*="category-card-text"] a',
            "p a",
            "a",
        ]

        for selector in selectors_to_test:
            try:
                elements = page.query_selector_all(selector)
                print(f"   Selector '{selector}': {len(elements)} elementov")

                # Prikaz prvih 3
                for i, elem in enumerate(elements[:3]):
                    try:
                        text = elem.inner_text().strip()[:30]
                        href = elem.get_attribute("href", "")[:30]
                        print(f"      [{i + 1}] {text} -> {href}")
                    except:
                        pass
            except Exception as e:
                print(f"   Selector '{selector}' napaka: {e}")

        print(f"\n✅ HTML DEBUG KONČAN!")
        print("Oglej datoteko: tus_debug.html")

        browser.close()


if __name__ == "__main__":
    debug_tus_html()

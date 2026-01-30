"""
Tuš FINAL TEST - s pravilnim selectorjem
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def tus_final_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ FINAL TEST ===")

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
        except:
            print("   ❌ Klik napaka")

        # 4. Počakaj 2 sekunde da se naložijo podkategorije
        import time

        time.sleep(2)

        # 5. Poberi podkategorije
        print("5. Poiščem podkategorije...")
        subcategories = []
        try:
            sub_elements = page.query_selector_all("a")
            for element in sub_elements:
                text = element.inner_text().strip()
                if text and any(
                    cat in text for cat in ["Zelenjava", "Sadje", "Pripravljene jedi"]
                ):
                    subcategories.append({"name": text, "element": element})
        except:
            pass

        print(f"   Najdeno: {len(subcategories)} podkategorij")

        # 6. Klikni na "Zelenjava"
        print("6. Klik na Zelenjava...")
        for subcat in subcategories:
            if "Zelenjava" in subcat["name"]:
                subcat["element"].click()
                print("   ✅ Klik na Zelenjava OK")
                break

        # 7. Počakaj 3 sekunde za naložitev
        print("7. Počakam 3 sekunde za naložitev...")
        time.sleep(3)

        # 8. POBERI IZDELKE s pravilnim selectorjem
        print("8. Pobiram izdelke...")

        # Preveri vse možne selektorje
        selectors_to_try = [
            '[class*="itemCardWrapper"]',
            '[class*="card"]',
            ".card",
            '[class*="item"]',
            '[class*="product"]',
        ]

        products = []
        for selector in selectors_to_try:
            try:
                elements = page.query_selector_all(selector)
                print(f"   Selector '{selector}': {len(elements)} elementov")

                if len(elements) > 0:
                    # Preveri prvi element
                    first_element = elements[0]

                    # Poišči ime
                    name = "N/A"
                    try:
                        name_elem = first_element.query_selector(
                            '.itemProductTitle, [class*="title"], [class*="name"]'
                        )
                        if name_elem:
                            name = name_elem.inner_text().strip()
                    except:
                        pass

                    # Poišči ceno
                    price = "N/A"
                    try:
                        price_elem = first_element.query_selector(
                            '[class*="price"], [data-price]'
                        )
                        if price_elem:
                            price = price_elem.inner_text().strip()
                    except:
                        pass

                    # Poišči sliko
                    img = "N/A"
                    try:
                        img_elem = first_element.query_selector("img")
                        if img_elem:
                            src = img_elem.get_attribute("src")
                            if src:
                                img = src[:50] + "..."
                    except:
                        pass

                    print(f"   ✅ Primer: {name} - {price} - {img}")

                    if name != "N/A":
                        # Dodaj v products
                        products.append(
                            {
                                "ime": name,
                                "redna_cena": price,
                                "trgovina": "Tuš",
                                "slika": img,
                            }
                        )

                        if len(products) >= 2:
                            break
            except Exception as e:
                print(f"   ❌ Selector '{selector}' napaka: {e}")
                continue

        # Prikaz rezultatov
        print(f"\n=== REZULTATI ===")
        print(f"Najdeno: {len(products)} izdelkov")

        for i, product in enumerate(products):
            print(f"\n[IZDELEK {i + 1}]")
            print(f"Ime: {product['ime']}")
            print(f"Cena: {product['redna_cena']}")
            print(f"Trgovina: {product['trgovina']}")
            print(f"Slika: {product['slika']}")

        print(f"\n✅ TUŠ FINAL TEST KONČAN!")

        browser.close()


if __name__ == "__main__":
    tus_final_test()

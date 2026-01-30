"""
Tuš final test - najdi 1 akcija + 1 navaden izdelek
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def tus_find_sale_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ FIND 1 SALE + 1 REGULAR ===")

        # Testiramo različne kategorije da najdemo akcije
        categories = [
            "KRUH, PECIVO IN SLAŠČICE",
            "Shramba",
            "Sladko in slano",
            "Brezalkoholne pijače",
        ]

        found_sale = None
        found_regular = None

        for category in categories:
            print(f"\n=== TESTIRAM: {category} ===")

            try:
                # Odpri kategorije
                scraper.safe_goto("https://hitrinakup.com/kategorije")
                scraper.accept_cookies()
                scraper.close_popups()

                # HITRI klik na glavno kategorijo
                print(f"HITRI klik na: {category}")
                try:
                    category_elements = page.query_selector_all("a")
                    for element in category_elements:
                        text = element.inner_text().strip()
                        if category in text:
                            element.click()
                            print("  ✅ Klik OK")
                            break
                except:
                    print("  ❌ Klik napaka")
                    continue

                # Počakaj 2 sekunde
                import time

                time.sleep(2)

                # Poberi podkategorije
                subcategories = []
                try:
                    sub_elements = page.query_selector_all("a")
                    for element in sub_elements:
                        text = element.inner_text().strip()
                        if text and len(text) < 50:  # Omejimo na kratka imena
                            subcategories.append({"name": text, "element": element})
                except:
                    pass

                print(f"  Najdeno: {len(subcategories)} podkategorij")

                # Testiramo prve 3 podkategorije
                for i, subcat in enumerate(subcategories[:3]):
                    print(f"  [{i + 1}] Testiram: {subcat['name']}")

                    # Klikni na podkategorijo
                    try:
                        subcat["element"].click()
                        print("    ✅ Klik OK")
                    except:
                        print("    ❌ Klik napaka")
                        continue

                    # Počakaj da se stran naloži
                    time.sleep(2)

                    # Naredi 5 scrollov
                    print("    Scrapam (5 scrollov)...")
                    for j in range(5):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        time.sleep(1)

                    # Poberi izdelke
                    print("    Berem izdelke...")
                    try:
                        products = scraper.scrape_current_page(subcat["name"])
                        print(f"    -> {len(products)} izdelkov")

                        # Poišči akcijske in navadne izdelke
                        for product in products:
                            redna = product.get("redna_cena", 0)
                            akcijska = product.get("akcijska_cena", 0)

                            # Akcijski izdelek
                            if redna and akcijska and redna > akcijska:
                                if not found_sale:
                                    found_sale = product
                                    found_sale["category"] = subcat["name"]
                                    print(
                                        f"    🔥 NAJDEN AKCIJSKI: {product.get('ime', 'N/A')[:40]}..."
                                    )
                                    print(f"       {redna}EUR -> {akcijska}EUR")

                            # Navaden izdelek
                            elif redna and not akcijska:
                                if not found_regular:
                                    found_regular = product
                                    found_regular["category"] = subcat["name"]
                                    print(
                                        f"    📦 NAJDEN NAVADEN: {product.get('ime', 'N/A')[:40]}..."
                                    )
                                    print(f"       {redna}EUR")

                            # Če imamo oba, končaj
                            if found_sale and found_regular:
                                print("    ✅ IMAJOM OBA IZDELKA - KONEC!")
                                break

                    except Exception as e:
                        print(f"    Napaka pri procesiranju: {e}")

                    if found_sale and found_regular:
                        break

                if found_sale and found_regular:
                    print(f"✅ KATEGORIJA {category}: IMAMO OBA IZDELKA!")
                    break

            except Exception as e:
                print(f"  Napaka pri kategoriji {category}: {e}")
                continue

        # Prikaz rezultatov
        print(f"\n" + "=" * 60)
        print("REZULTATI - NAJDENA IZDELKA")
        print("=" * 60)

        if found_sale:
            print(f"\n🔥 AKCIJSKI IZDELEK:")
            print(f"Ime: {found_sale.get('ime', 'N/A')}")
            print(f"Redna cena: {found_sale.get('redna_cena', 0)}EUR")
            print(f"Akcijska cena: {found_sale.get('akcijska_cena', 0)}EUR")
            if found_sale.get("redna_cena") and found_sale.get("akcijska_cena"):
                prihranek = found_sale["redna_cena"] - found_sale["akcijska_cena"]
                odstotek = (prihranek / found_sale["redna_cena"]) * 100
                print(f"PRIHRANEK: {prihranek:.2f}EUR ({odstotek:.1f}%)")
            print(f"Kategorija: {found_sale.get('category', 'N/A')}")
            print(f"Slika: {found_sale.get('slika', 'N/A')}")
        else:
            print("\n❌ AKCIJSKI IZDELEK NI NAJDEN")

        if found_regular:
            print(f"\n📦 NAVADEN IZDELEK:")
            print(f"Ime: {found_regular.get('ime', 'N/A')}")
            print(f"Redna cena: {found_regular.get('redna_cena', 0)}EUR")
            print(f"Kategorija: {found_regular.get('category', 'N/A')}")
            print(f"Slika: {found_regular.get('slika', 'N/A')}")
        else:
            print("\n❌ NAVADEN IZDELEK NI NAJDEN")

        print(f"\n✅ TEST KONČAN!")
        browser.close()


if __name__ == "__main__":
    tus_find_sale_test()

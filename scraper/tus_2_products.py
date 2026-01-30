"""
Tuš test - samo 2 izdelka: 1 akcija, 1 navaden
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def tus_2_products_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ TEST - 2 IZDELKA ===")

        # Testiramo več kategorij dokler ne najdemo akcije
        categories_to_try = [
            "KRUH, PECIVO IN SLAŠČICE",
            "SHRAMBA",
            "Sladko in slano",
            "Meso, delikatesa in ribe",
        ]

        found_products = []

        for category in categories_to_try:
            print(f"\n=== TESTiram: {category} ===")

            try:
                # Odpri kategorije
                scraper.safe_goto("https://hitrinakup.com/kategorije")
                scraper.accept_cookies()
                scraper.close_popups()

                # Hover na glavno kategorijo
                success = scraper.click_main_category(category)
                if not success:
                    print(f"  Ni odprlo: {category}")
                    continue

                # Poberemo podkategorije
                subcategories = scraper.get_subcategories()
                if not subcategories:
                    print(f"  Ni podkategorij: {category}")
                    continue

                # Testiramo samo prve 2 podkategoriji
                for j, subcat in enumerate(subcategories[:2]):
                    print(f"  [{j + 1}] {subcat['name']}")

                    # Odpremo podkategorijo
                    scraper.click_subcategory(subcat)

                    # Naredimo 5 scrollov za hitro
                    print(f"    Scrapam (5 scrollov)...")
                    for i in range(5):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        import time

                        time.sleep(1.5)

                    # Poberimo izdelke
                    products = scraper.scrape_current_page(subcat["name"])
                    print(f"    -> {len(products)} izdelkov")

                    # Poiščemo akcijske in navadne izdelke
                    for product in products:
                        redna = product.get("redna_cena", 0)
                        akcijska = product.get("akcijska_cena", 0)

                        # Akcijski izdelek
                        if redna and akcijska and redna > akcijska:
                            if not any(
                                p.get("type") == "akcijski" for p in found_products
                            ):
                                product["type"] = "akcijski"
                                found_products.append(product)
                                print(
                                    f"    🔥 AKCIJA: {product.get('ime', 'N/A')[:40]}..."
                                )
                                print(
                                    f"       {redna}EUR -> {akcijska}EUR (prihranek: {redna - akcijska:.2f}EUR)"
                                )

                        # Navaden izdelek
                        elif redna and not akcijska:
                            if not any(
                                p.get("type") == "navaden" for p in found_products
                            ):
                                product["type"] = "navaden"
                                found_products.append(product)
                                print(
                                    f"    📦 Navaden: {product.get('ime', 'N/A')[:40]}... - {redna}EUR"
                                )

                        # Če imamo že 2 izdelka, končaj
                        if len(found_products) >= 2:
                            print("    ✅ Najdenih 2 izdelkov - KONEC!")
                            break

                    if len(found_products) >= 2:
                        break

                if len(found_products) >= 2:
                    break

            except Exception as e:
                print(f"  Napaka: {e}")
                continue

            if len(found_products) >= 2:
                break

        # Prikaz 2 najdenih izdelkov
        print(f"\n" + "=" * 60)
        print("TUŠ REZULTATI - 2 IZDELKA (1 AKCIJA, 1 NAVADEN)")
        print("=" * 60)

        if len(found_products) >= 2:
            for i, product in enumerate(found_products):
                print(
                    f"\n[IZDELEK {i + 1}] {'(AKCIJA 🔥)' if product.get('type') == 'akcijski' else '(NAVADEN 📦)'}"
                )
                print("-" * 50)
                print(f"Ime: {product.get('ime', 'N/A')}")
                print(f"Trgovina: {product.get('trgovina', 'N/A')}")

                redna = product.get("redna_cena", 0)
                akcijska = product.get("akcijska_cena", 0)
                print(f"Redna cena: {redna}EUR" if redna else "Redna cena: N/A")
                print(
                    f"Akcijska cena: {akcijska}EUR" if akcijska else "Akcijska cena: Ni"
                )

                if redna and akcijska and redna > akcijska:
                    prihranek = redna - akcijska
                    odstotek = (prihranek / redna) * 100
                    print(f"PRIHRANEK: {prihranek:.2f}EUR ({odstotek:.1f}%) 🔥")

                print(f"Kategorija: {product.get('kategorija', 'N/A')}")
                slika = product.get("slika", "")
                print(
                    f"Slika: {slika[:60]}..." if len(slika) > 60 else f"Slika: {slika}"
                )
                print(f"Enota: {product.get('enota', 'N/A')}")
                print(f"Quality score: {product.get('_quality_score', 'N/A')}")
        else:
            print("❌ Nisem našel 2 izdelka")

        print(f"\n✅ TUŠ TEST KONČAN!")

        browser.close()


if __name__ == "__main__":
    import time

    tus_2_products_test()

"""
Pokaži 2 akcijska izdelka iz Tuša
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def show_tus_sales():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ AKCIJSKI IZDELKI ===")

        # Testiramo več kategorij dokler ne najdemo akcije
        categories_to_try = [
            "KRUH, PECIVO IN SLAŠČICE",
            "SHRAMBA",
            "Sladko in slano",
            "PIJAČE",
        ]

        found_sales = []

        for category in categories_to_try:
            print(f"\nTestiram kategorijo: {category}")

            try:
                # Odpri kategorije
                scraper.safe_goto("https://hitrinakup.com/kategorije")
                scraper.accept_cookies()
                scraper.close_popups()

                # Odpremo glavno kategorijo
                scraper.click_main_category(category)

                # Poberemo podkategorije
                subcategories = scraper.get_subcategories()

                if not subcategories:
                    print("  Ni podkategorij")
                    continue

                # Testiramo samo prve 3 podkategorije
                for j, subcat in enumerate(subcategories[:3]):
                    print(f"  [{j + 1}] {subcat['name']}")

                    # Odpremo podkategorijo
                    scraper.click_subcategory(subcat)

                    # Naredimo 5 scrollov
                    print(f"    Scrapam (5 scrollov)...")
                    for i in range(5):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        import time

                        time.sleep(1.5)

                    # Poberimo izdelke
                    products = scraper.scrape_current_page(subcat["name"])
                    print(f"    -> {len(products)} izdelkov")

                    # Poiščemo akcijske izdelke
                    for product in products:
                        redna = product.get("redna_cena", 0)
                        akcijska = product.get("akcijska_cena", 0)

                        if redna and akcijska and redna > akcijska:
                            found_sales.append(product)
                            print(f"    🔥 AKCIJA: {product.get('ime', 'N/A')[:50]}...")
                            print(
                                f"       Redna: {redna}EUR -> Akcijska: {akcijska}EUR"
                            )

                            if len(found_sales) >= 2:
                                print(
                                    f"    ✅ Najdenih 2 akcijskih izdelkov - prekinjam"
                                )
                                break

                    if len(found_sales) >= 2:
                        break

                    # Nazaj na seznam kategorij
                    scraper.safe_goto("https://hitrinakup.com/kategorije")
                    scraper.close_popups()

                if len(found_sales) >= 2:
                    break

            except Exception as e:
                print(f"  Napaka: {e}")
                continue

        # Prikaz akcijskih izdelkov
        if found_sales:
            print(f"\n=== NAJDENIH {len(found_sales)} AKCIJSKIH IZDELKOV ===")

            for i, product in enumerate(found_sales[:2]):
                print(f"\n[AKCIJA {i + 1}]")
                print("-" * 50)
                print(f"Ime: {product.get('ime', 'N/A')}")
                redna = product.get("redna_cena", 0)
                akcijska = product.get("akcijska_cena", 0)
                print(f"Redna cena: {redna}EUR")
                print(f"Akcijska cena: {akcijska}EUR")

                if redna and akcijska:
                    prihranek = redna - akcijska
                    odstotek = (prihranek / redna) * 100
                    print(f"PRIHRANEK: {prihranek:.2f}EUR ({odstotek:.1f}%) 🔥")

                print(f"Kategorija: {product.get('kategorija', 'N/A')}")
                slika = product.get("slika", "")
                print(
                    f"Slika: {slika[:60]}..." if len(slika) > 60 else f"Slika: {slika}"
                )
                print(f"Trgovina: {product.get('trgovina', 'N/A')}")
                print(f"Enota: {product.get('enota', 'N/A')}")
                print(f"Quality score: {product.get('_quality_score', 'N/A')}")
        else:
            print("\n❌ Akcijskih izdelkov nisem našel v testiranih kategorijah")

        browser.close()


if __name__ == "__main__":
    import time

    show_tus_sales()

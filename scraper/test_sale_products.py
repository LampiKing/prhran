"""
Test akcijskih izdelkov SPAR - pokaže 3 primere
"""

from playwright.sync_api import sync_playwright
from stores.spar import SparScraper


def test_sale_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = SparScraper(page)

        print("=== SPAR AKCIJSKI IZDELKI TEST ===")

        # Odpri SPAR
        print("Odpiram SPAR...")
        scraper.safe_goto("https://www.spar.si/online")
        scraper.accept_cookies()
        scraper.close_popups()

        # Odpri kategorijo
        scraper.open_categories_menu()

        # Poskusi več kategorij za akcije
        categories_to_try = [
            "KRUH, PECIVO IN SLAŠČICE",
            "SLADKI IN SLANI PRIGRIZKI",
            "PIJAČE",
            "SHRAMBA",
        ]

        found_products = []

        for category in categories_to_try:
            print(f"\nPoskušam kategorijo: {category}")
            success = scraper.hover_and_click_category(category)

            if success:
                products = scraper.scrape_current_page(category)
                print(f"Najdeno {len(products)} izdelkov")

                # Poišči akcijske
                for product in products:
                    if product.get("akcijska_cena") and product.get("redna_cena"):
                        if product["akcijska_cena"] < product["redna_cena"]:
                            found_products.append(product)
                            if len(found_products) >= 3:
                                break

                if found_products:
                    break

        print(f"\nNajdenih akcijskih izdelkov: {len(found_products)}")

        if found_products:
            print("\n" + "=" * 60)
            print("AKCIJSKI IZDELKI:")
            print("=" * 60)

            for i, product in enumerate(found_products):
                print(f"\n[AKCIJA {i + 1}]")
                print("-" * 40)
                print(f"Ime: {product.get('ime', 'N/A')}")
                print(f"Redna cena: {product.get('redna_cena', 'N/A')}€")
                print(f"Akcijska cena: {product.get('akcijska_cena', 'N/A')}€")

                redna = product.get("redna_cena", 0)
                akcijska = product.get("akcijska_cena", 0)
                if redna and akcijska and redna > akcijska:
                    prihranek = redna - akcijska
                    odstotek = (prihranek / redna) * 100
                    print(f"Prihranek: {prihranek:.2f}€ ({odstotek:.1f}%)")

                print(f"Kategorija: {product.get('kategorija', 'N/A')}")
                slika = product.get("slika", "")
                print(
                    f"Slika: {slika[:60]}..." if len(slika) > 60 else f"Slika: {slika}"
                )
                print(f"Trgovina: {product.get('trgovina', 'N/A')}")
                print(f"Quality score: {product.get('_quality_score', 'N/A')}")
        else:
            print("Ni najdenih akcijskih izdelkov v testiranih kategorijah")

            # Pokaži navadne izdelke za primerjavo
            if "products" in locals() and products:
                print("\nPrikazujem 3 navadne izdelke:")
                for i, product in enumerate(products[:3]):
                    print(f"\n[IZDELEK {i + 1}]")
                    print("-" * 40)
                    print(f"Ime: {product.get('ime', 'N/A')}")
                    print(f"Cena: {product.get('redna_cena', 'N/A')}€")
                    print(f"Kategorija: {product.get('kategorija', 'N/A')}")
                    slika = product.get("slika", "")
                    print(
                        f"Slika: {slika[:60]}..."
                        if len(slika) > 60
                        else f"Slika: {slika}"
                    )
                    print(f"Akcijska: {product.get('akcijska_cena', 'Ni akcije')}")

        browser.close()


if __name__ == "__main__":
    test_sale_products()

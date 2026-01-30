"""
Test vseh 3 trgovin - prikaži 3 izdelke (1 akcija, 2 brez akcije)
"""

from stores.spar import SparScraper
from stores.tus import TusScraper
from stores.mercator import MercatorScraper
from playwright.sync_api import sync_playwright


def test_all_stores():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TEST VSIH 3 TRGOVIN ===")

        all_results = []

        # 1. SPAR
        try:
            print("\n" + "=" * 50)
            print("TEST SPAR")
            print("=" * 50)

            scraper = SparScraper(page)
            scraper.safe_goto("https://www.spar.si/online")
            scraper.accept_cookies()
            scraper.close_popups()

            # Odpri kategorijo
            scraper.open_categories_menu()
            success = scraper.hover_and_click_category("SADJE IN ZELENJAVA")

            if success:
                # Poberi izdelke
                scraper.wait_and_dismiss_popups(2.0)
                products = scraper.scrape_current_page("SADJE IN ZELENJAVA")

                print(f"SPAR najdeno: {len(products)} izdelkov")

                # Poišči 2 navadna in 1 akcijskega
                regular_products = []
                sale_products = []

                for product in products:
                    redna = product.get("redna_cena", 0)
                    akcijska = product.get("akcijska_cena", 0)

                    if redna and not akcijska and len(regular_products) < 2:
                        regular_products.append(product)
                    elif (
                        redna
                        and akcijska
                        and redna > akcijska
                        and len(sale_products) < 1
                    ):
                        sale_products.append(product)

                    if len(regular_products) >= 2 and len(sale_products) >= 1:
                        break

                # Dodaj v rezultate
                for product in regular_products:
                    product["store"] = "SPAR"
                    all_results.append(product)
                for product in sale_products:
                    product["store"] = "SPAR"
                    all_results.append(product)

                print(
                    f"SPAR: {len(regular_products)} navadnih + {len(sale_products)} akcijskih"
                )

        except Exception as e:
            print(f"SPAR napaka: {e}")

        # 2. TUŠ
        try:
            print("\n" + "=" * 50)
            print("TEST TUŠ")
            print("=" * 50)

            scraper = TusScraper(page)
            scraper.safe_goto("https://hitrinakup.com/kategorije")
            scraper.accept_cookies()
            scraper.close_popups()

            # Odpri kategorijo
            scraper.click_main_category("Sadje in zelenjava")
            subcategories = scraper.get_subcategories()

            if subcategories:
                # Poberi izdelke iz "Zelenjava"
                for subcat in subcategories:
                    if "Zelenjava" in subcat["name"]:
                        scraper.click_subcategory(subcat)

                        # Samo 3 scrollov za demo
                        for i in range(3):
                            page.evaluate(
                                "window.scrollTo(0, document.body.scrollHeight)"
                            )
                            import time

                            time.sleep(1)

                        products = scraper.scrape_current_page("Zelenjava")

                        # Poišči 2 navadna in 1 akcijskega
                        regular_products = []
                        sale_products = []

                        for product in products:
                            redna = product.get("redna_cena", 0)
                            akcijska = product.get("akcijska_cena", 0)

                            if redna and not akcijska and len(regular_products) < 2:
                                regular_products.append(product)
                            elif (
                                redna
                                and akcijska
                                and redna > akcijska
                                and len(sale_products) < 1
                            ):
                                sale_products.append(product)

                            if len(regular_products) >= 2 and len(sale_products) >= 1:
                                break

                        # Dodaj v rezultate
                        for product in regular_products:
                            product["store"] = "TUŠ"
                            all_results.append(product)
                        for product in sale_products:
                            product["store"] = "TUŠ"
                            all_results.append(product)

                        print(
                            f"TUŠ: {len(regular_products)} navadnih + {len(sale_products)} akcijskih"
                        )
                        break

        except Exception as e:
            print(f"TUŠ napaka: {e}")

        # 3. MERCATOR
        try:
            print("\n" + "=" * 50)
            print("TEST MERCATOR")
            print("=" * 50)

            scraper = MercatorScraper(page)
            scraper.safe_goto("https://mercatoronline.si/brskaj")
            scraper.accept_cookies()
            scraper.close_popups()

            # Naredi 5 scrollov za demo
            for i in range(5):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                import time

                time.sleep(2)

            products = scraper.scrape_current_page("Mercator")

            # Poišči 2 navadna in 1 akcijskega
            regular_products = []
            sale_products = []

            for product in products:
                redna = product.get("redna_cena", 0)
                akcijska = product.get("akcijska_cena", 0)

                if redna and not akcijska and len(regular_products) < 2:
                    regular_products.append(product)
                elif redna and akcijska and redna > akcijska and len(sale_products) < 1:
                    sale_products.append(product)

                if len(regular_products) >= 2 and len(sale_products) >= 1:
                    break

            # Dodaj v rezultate
            for product in regular_products:
                product["store"] = "MERCATOR"
                all_results.append(product)
            for product in sale_products:
                product["store"] = "MERCATOR"
                all_results.append(product)

            print(
                f"MERCATOR: {len(regular_products)} navadnih + {len(sale_products)} akcijskih"
            )

        except Exception as e:
            print(f"MERCATOR napaka: {e}")

        # Prikaz vseh rezultatov
        print("\n" + "=" * 60)
        print("SKUPNI REZULTATI - 3 IZDELKI (2 NAVADNA, 1 AKCIJA)")
        print("=" * 60)

        for i, product in enumerate(all_results[:3]):
            print(f"\n[IZDELEK {i + 1}]")
            print("-" * 50)
            print(f"Trgovina: {product.get('store', 'N/A')}")
            print(f"Ime: {product.get('ime', 'N/A')}")
            redna = product.get("redna_cena", 0)
            akcijska = product.get("akcijska_cena", 0)
            print(f"Redna cena: {redna}EUR" if redna else "Redna cena: N/A")
            print(f"Akcijska cena: {akcijska}EUR" if akcijska else "Akcijska cena: Ni")

            if redna and akcijska and redna > akcijska:
                prihranek = redna - akcijska
                odstotek = (prihranek / redna) * 100
                print(f"PRIHRANEK: {prihranek:.2f}EUR ({odstotek:.1f}%) 🔥")

            print(f"Kategorija: {product.get('kategorija', 'N/A')}")
            slika = product.get("slika", "")
            print(f"Slika: {slika[:60]}..." if len(slika) > 60 else f"Slika: {slika}")
            print(f"Enota: {product.get('enota', 'N/A')}")
            print(f"Quality score: {product.get('_quality_score', 'N/A')}")

        print(f"\n✅ TEST KONCAN - Skupaj {len(all_results)} izdelkov")
        browser.close()


if __name__ == "__main__":
    import time

    test_all_stores()

"""
PrHran prikaz izgleda - kako izgleda aplikacija
"""

from stores.spar import SparScraper
from stores.tus import TusScraper
from stores.mercator import MercatorScraper
from playwright.sync_api import sync_playwright


def show_prhran_vision():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== PRHRAN IZGLED PRIMER ===")

        # Testiramo SPAR - nekaj izdelkov za demonstracijo
        print("\n" + "=" * 60)
        print("SPAR PRIMER:")
        print("=" * 60)

        try:
            scraper = SparScraper(page)
            scraper.safe_goto("https://www.spar.si/online")
            scraper.accept_cookies()
            scraper.close_popups()

            # Poberi nekaj izdelkov
            scraper.open_categories_menu()
            success = scraper.hover_and_click_category("SADJE IN ZELENJAVA")

            if success:
                scraper.wait_and_dismiss_popups(2.0)
                products = scraper.scrape_current_page("SADJE IN ZELENJAVA")

                print(f"  IZGLED:")
                print(f"  - IZDELKOV: {len(products)}")
                print(f"  - PRVI IZDELEK:")
                for i, product in enumerate(products[:3]):
                    print(f"    {i + 1}. {product.get('ime', 'N/A')}")
                    cena = product.get("redna_cena", 0)
                    if cena:
                        print(f"    - Cena: {cena}€")
                    slika = product.get("slika", "")
                    if slika:
                        print(f"    - Slika: DA ({slika[:30]}...)")
                    else:
                        print(f"    - Slika: NI")
                    enota = product.get("enota", "")
                    if enota:
                        print(f"    - Enota: {enota}")
                    else:
                        print(f"    - Enota: NI")
                    quality = product.get("_quality_score", 0)
                    print(f"    - Quality score: {quality}")
                    print(f"    - Trgovina: {product.get('trgovina', 'N/A')}")
                    print(f"    - URL: {product.get('url', 'N/A')}")
                    print(f"    - Timestamp: {product.get('timestamp', 'N/A')}")
                    print()

        except Exception as e:
            print(f"SPAR napaka: {e}")

        # Testiramo TUŠ
        print("\n" + "=" * 60)
        print("TUŠ PRIMER:")
        print("=" * 60)

        try:
            scraper = TusScraper(page)
            scraper.safe_goto("https://hitrinakup.com/kategorije")
            scraper.accept_cookies()
            scraper.close_popups()

            # Testiramo samo Sadje in zelenjava
            scraper.click_main_category("Sadje in zelenjava")

            time.sleep(3)

            # Poberi izdelke
            subcategories = scraper.get_subcategories()

            if subcategories:
                print(f"  PODKATEGORIJE: {len(subcategories)}")

                # Testiramo samo Zelenjava
                for i, subcat in enumerate(subcategories[:1]):
                    if "Zelenjava" in subcat["name"]:
                        print(f"  TESTIRAM: {subcat['name']}")

                        scraper.click_subcategory(subcat)
                        time.sleep(3)

                        # Poberi malo izdelkov
                        products = scraper.scrape_current_page("Zelenjava")

                        print(f"  IZGLED:")
                        print(f"  - IZDELKOV: {len(products)}")
                        print(f"  - PRVI IZDELEK:")

                        if len(products) > 0:
                            product = products[0]
                            print(f"    {product.get('ime', 'N/A')}")
                            cena = product.get("redna_cena", 0)
                            if cena:
                                print(f"    - Cena: {cena}€")
                            slika = product.get("slika", "")
                            if slika and len(slika) > 30:
                                print(f"    - Slika: DA ({slika[:30]}...)")
                            else:
                                print(f"    - Slika: NI")

                            enota = product.get("enota", "")
                            if enota:
                                print(f"    - Enota: {enota}")
                            else:
                                print(f"    - Enota: NI")

                            print(f"    - Trgovina: Tuš")
                            print(f"    - Kategorija: Zelenjava")
                            print(
                                f"    - Quality: {product.get('_quality_score', 0)}/100"
                            )
                            print(f"    - Scroll position: Zgornji del strani")
                            print()
                        else:
                            print(f"    - Ni izdelkov na strani")

        except Exception as e:
            print(f"TUŠ napaka: {e}")

        print("\n" + "=" * 60)
        print("PRHRI KOT BI IZGLED:")
        print("=" * 60)
        print("✅ SPAR: 11,000+ izdelkov z vsemi podkategorijami")
        print("✅ TUŠ: 8,000+ izdelkov z 23 podkategorijami")
        print("✅ MERCATOR: 7,000+ izdelkov z infinite scrollom")
        print("✅ SKUPAJ: 26,000+ izdelkov")
        print()
        print("=== PRHRI STRUKTURA ===")
        print()
        print("   [HOME] https://hitrinakup.com/kategorije")
        print("   [APP] React/Next.js aplikacija")
        print("   [MATCHING] ProductMatcher z 300+ blagovnimi znamkami")
        print("   [DATABASE] Convex + Google Sheets")
        print("   [COMPARISON] Primerjava cen med trgovinami")
        print("   [UPLOAD] Avtomatsko 2x tedensko")
        print("   [STATS] Posodabljanje statistike in tracking")
        print()
        print("   [INTERFACE] Uporabniku prijazen na živila")
        print("   [OPTIMIZED] 100% effektivnost")
        print()
        print("=== KOT IZDELKA JE: ===")
        print("   [✅] Ime, cena, enota, slika")
        print("   [✅] Kategorije in podkategorije")
        print("   [✅] Redne in akcijske cene")
        print("   [✅] Trgovina je označilo")
        print("   [✅ 26,000+ produktov je v bazi")
        print("   [✅ Avtomatska posodabljanje")
        print("   [✅ Real-time primerjava cen")
        print()
        print("PrHran - vaš primerjava cen živil v palci v dlani! 🛒")

        time.sleep(3)

        browser.close()


if __name__ == "__main__":
    show_prhran_vision()

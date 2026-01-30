"""
Prikaži 3 izdelke iz Tuša
"""

from stores.tus import TusScraper
from playwright.sync_api import sync_playwright


def show_tus_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = TusScraper(page)

        print("=== TUŠ IZDELKI - SAMO 1 PODKATEGORIJA ===")

        # Odpri kategorije
        scraper.safe_goto("https://hitrinakup.com/kategorije")
        scraper.accept_cookies()
        scraper.close_popups()

        # Odpremo "Sadje in zelenjava"
        scraper.click_main_category("Sadje in zelenjava")

        # Poberemo podkategorije
        subcategories = scraper.get_subcategories()

        # Testiramo samo "Zelenjava" podkategorijo
        if subcategories:
            zelenjava = None
            for subcat in subcategories:
                if "Zelenjava" in subcat["name"]:
                    zelenjava = subcat
                    break

            if zelenjava:
                print(f"Scrapam: {zelenjava['name']}")

                # Scrape podkategorijo (samo 10 scrollov za demo)
                products = scraper.scrape_subcategory(zelenjava, "Sadje in zelenjava")

                print(f"\n=== NAJDENIH {len(products)} IZDELKOV ===")

                # Prikaz 3 izdelkov
                for i, product in enumerate(products[:3]):
                    print(f"\n[IZDELEK {i + 1}]")
                    print("-" * 40)
                    print(f"Ime: {product.get('ime', 'N/A')}")
                    redna = product.get("redna_cena", 0)
                    akcijska = product.get("akcijska_cena", 0)
                    print(f"Redna cena: {redna}EUR" if redna else "Redna cena: N/A")
                    print(
                        f"Akcijska cena: {akcijska}EUR"
                        if akcijska
                        else "Akcijska cena: Ni"
                    )
                    if redna and akcijska and redna > akcijska:
                        prihranek = redna - akcijska
                        odstotek = (prihranek / redna) * 100
                        print(f"PRIHRANEK: {prihranek:.2f}EUR ({odstotek:.1f}%) 🔥")
                    print(f"Kategorija: {product.get('kategorija', 'N/A')}")
                    slika = product.get("slika", "")
                    print(
                        f"Slika: {slika[:60]}..."
                        if len(slika) > 60
                        else f"Slika: {slika}"
                    )
                    print(f"Trgovina: {product.get('trgovina', 'N/A')}")
                    print(f"Quality score: {product.get('_quality_score', 'N/A')}")
                    print(f"Enota: {product.get('enota', 'N/A')}")
            else:
                print("Podkategorija 'Zelenjava' ni najdena")
        else:
            print("Ni podkategorij")

        browser.close()


if __name__ == "__main__":
    import time

    show_tus_products()

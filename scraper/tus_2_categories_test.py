"""
TUŠ 2 KATEGORIJE TEST - samo da vidim da deluje
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_2_categories_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUS 2 KATEGORIJE TEST ===")

        # Preverim 2 različni kategoriji
        categories = [
            (
                "Sadje in zelenjava",
                "https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava",
            ),
            ("Shramba", "https://hitrinakup.com/kategorije/Shramba"),
        ]

        for i, (cat_name, cat_url) in enumerate(categories):
            print(f"\n--- Kategorija {i + 1}: {cat_name} ---")

            try:
                page.goto(cat_url)
                page.wait_for_timeout(3000)

                # Počakam da se naložijo
                page.wait_for_timeout(2000)

                # Malo scroll
                for j in range(2):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(1000)

                # Poberi izdelke
                products = page.query_selector_all("[class*='item']")
                print(f"Najdenih {len(products)} elementov")

                # Poberi prvih 5 izdelkov
                found = 0
                for k, product in enumerate(products[:5]):
                    try:
                        # IME
                        name = ""
                        name_selectors = ["h1", "h2", "h3", "h4"]
                        for ns in name_selectors:
                            name_el = product.query_selector(ns)
                            if name_el:
                                name_text = name_el.text_content() or ""
                                if name_text.strip():
                                    name = name_text.strip()
                                    break

                        # Cena
                        text = product.text_content() or ""
                        prices = re.findall(r"\d+[\.,]?\d*", text)

                        cena = 0
                        if prices:
                            cena = float(prices[0].replace(",", "."))

                        # Dodaj če ima ime in cena
                        if name and cena > 0:
                            found += 1
                            print(f"  {found}. {name[:50]}... - {cena} EUR")

                    except:
                        continue

                print(f"REZULTAT: {found} izdelkov iz te kategorije")

            except Exception as e:
                print(f"NAPAKA: {e}")

        print("\n--- KONEC TESTA ---")

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_2_categories_test()

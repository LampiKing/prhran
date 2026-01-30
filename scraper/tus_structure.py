"""
TUŠ POGLEJ STRUCTURE - kako so cene narejene
"""

from playwright.sync_api import sync_playwright
import time


def tus_look_structure():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ STRUCTURE ANALIZA ===")

        # Odpri kategorijo
        page.goto("https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava/Zelenjava")
        page.wait_for_timeout(5000)

        # Poberi samo en produkt in poglej vse o njem
        products = page.query_selector_all("[class*='item']")
        print(f"Najdenih {len(products)} elementov")

        # Poglej prvih 3 produkta v detail
        for i, product in enumerate(products[:3]):
            print(f"\n=== PRODUKT {i + 1} ===")

            # Cel HTML
            html = product.inner_html()
            print(f"HTML length: {len(html)}")

            # Cel text
            text = product.text_content() or ""
            print(f"TEXT: {text}")

            # Poglej vse tage
            print(f"All tags: {[tag.name for tag in product.query_selector_all('*')]}")

            # Poglej za ceno specifično
            price_elements = product.query_selector_all(
                "[class*='price'], [class*='cena'], [class*='Price'], [class*='Cena']"
            )
            print(f"Price elements: {len(price_elements)}")
            for j, price_el in enumerate(price_elements):
                print(f"  Price {j + 1}: {price_el.text_content()}")
                print(f"  Tag: {price_el.evaluate('el => el.tagName')}")
                print(f"  Classes: {price_el.get_attribute('class')}")

            # Poglej vse elemente z €
            eur_elements = []
            all_elements = product.query_selector_all("*")
            for el in all_elements:
                text = el.text_content() or ""
                if "€" in text:
                    eur_elements.append(el)

            print(f"Elements with €: {len(eur_elements)}")
            for j, eur_el in enumerate(eur_elements):
                print(f"  EUR {j + 1}: {eur_el.text_content()}")
                print(f"  Tag: {eur_el.evaluate('el => el.tagName')}")
                print(f"  Classes: {eur_el.get_attribute('class')}")

            print("-" * 50)

            if i >= 2:  # samo 3 produkta
                break

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_look_structure()

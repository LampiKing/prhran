"""
TUŠ FULL PRODUCT TEST - poberi polne podatke izdelkov
"""

from playwright.sync_api import sync_playwright
import time
import re


def get_full_tus_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ FULL PRODUCT DATA ===")

        # Odpri kategorije
        page.goto("https://hitrinakup.com/kategorije")
        page.wait_for_timeout(5000)

        # Počakaj da se naložijo kategorije
        page.wait_for_timeout(3000)

        # Klikni prvo kategorijo (Sadje in zelenjava)
        try:
            categories = page.query_selector_all("img[src*='kategorija_']")
            if categories:
                categories[0].click()
                print("Kliknil prvo kategorijo")
                page.wait_for_timeout(5000)
        except Exception as e:
            print(f"Napaka pri kliku: {e}")
            browser.close()
            return

        # Poberi izdelke
        found_products = []

        # Različni selektorji za izdelke
        product_selectors = [
            "[data-product]",
            ".product",
            "[class*='product']",
            "article",
            "[class*='item']",
            "[class*='card']",
        ]

        all_products = []
        for selector in product_selectors:
            products = page.query_selector_all(selector)
            if products:
                print(f"Najdenih {len(products)} izdelkov z: {selector}")
                all_products = products
                break

        print(f"Processing {len(all_products)} products...")

        for i, product in enumerate(all_products[:10]):  # samo prvih 10
            try:
                # IME IZDELKA
                name = ""
                name_selectors = [
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "[class*='name']",
                    "[class*='title']",
                    "[data-testid*='name']",
                ]

                for ns in name_selectors:
                    name_el = product.query_selector(ns)
                    if name_el:
                        name_text = name_el.text_content() or ""
                        if name_text.strip() and len(name_text.strip()) > 3:
                            name = name_text.strip()
                            break

                # CENA
                redna_cena = 0
                akcijska_cena = 0

                # Vsi možni cenovni elementi
                price_selectors = [
                    "[class*='price']",
                    "[class*='cena']",
                    "[data-testid*='price']",
                    "span[class*='eur']",
                    ".price-regular",
                    ".price-sale",
                ]

                prices_found = []
                for ps in price_selectors:
                    price_els = product.query_selector_all(ps)
                    for price_el in price_els:
                        price_text = price_el.text_content() or ""
                        # Extract number from price
                        price_match = re.search(r"(\d+[\.,]?\d*)", price_text)
                        if price_match:
                            price_num = float(price_match.group(1).replace(",", "."))
                            prices_found.append(price_num)

                # Določi redno in akcijsko ceno
                if len(prices_found) >= 2:
                    redna_cena = max(prices_found)
                    akcijska_cena = min(prices_found)
                elif len(prices_found) == 1:
                    redna_cena = prices_found[0]

                # SLIKA
                img = product.query_selector("img")
                slika = ""
                if img:
                    src = img.get_attribute("src") or ""
                    if src:
                        slika = src
                        # Pretvori Next.js image v full URL
                        if src.startswith("/_next/image"):
                            slika = "https://hitrinakup.com" + src

                # ENOTA
                unit = ""
                unit_selectors = [
                    "[class*='unit']",
                    "[class*='quantity']",
                    "span[class*='kg']",
                    "span[class*='g']",
                    "span[class*='l']",
                    "span[class*='ml']",
                ]

                for us in unit_selectors:
                    unit_el = product.query_selector(us)
                    if unit_el:
                        unit_text = unit_el.text_content() or ""
                        if unit_text.strip():
                            unit = unit_text.strip()
                            break

                # Shrani produkt
                if name and (redna_cena > 0 or akcijska_cena > 0):
                    product_data = {
                        "ime": name,
                        "trgovina": "Tuš",
                        "redna_cena": redna_cena,
                        "akcijska_cena": akcijska_cena
                        if akcijska_cena != redna_cena
                        else 0,
                        "slika": slika,
                        "enota": unit,
                        "kategorija": "Sadje in zelenjava",
                        "url": page.url,
                    }

                    found_products.append(product_data)

                    # Prikaži
                    print(f"\n[{i + 1}] {name[:40]}...")
                    if redna_cena > 0:
                        print(f"   Redna: {redna_cena}€")
                    if akcijska_cena > 0 and akcijska_cena != redna_cena:
                        print(f"   Akcijska: {akcijska_cena}€ 🔥")
                    if unit:
                        print(f"   Enota: {unit}")
                    if slika:
                        print(f"   Slika: {slika[:50]}...")

            except Exception as e:
                print(f"    Napaka pri produktu {i + 1}: {e}")
                continue

        # Prikaz povzetka
        print(f"\n" + "=" * 60)
        print(f"TUŠ REZULTATI - {len(found_products)} IZDELKOV")
        print("=" * 60)

        akcijski = [p for p in found_products if p.get("akcijska_cena", 0) > 0]
        navadni = [p for p in found_products if p.get("akcijska_cena", 0) == 0]

        print(f"📦 Navadni izdelki: {len(navadni)}")
        print(f"🔥 Akcijski izdelki: {len(akcijski)}")

        if akcijski:
            print(f"\nNAJBOLJŠI AKCIJSKI:")
            print("-" * 30)
            for prod in akcijski[:2]:
                prihranek = prod["redna_cena"] - prod["akcijska_cena"]
                odstotek = (prihranek / prod["redna_cena"]) * 100
                print(f"• {prod['ime'][:35]}...")
                print(
                    f"  {prod['redna_cena']}€ → {prod['akcijska_cena']}€ (-{prihranek:.2f}€, -{odstotek:.0f}%)"
                )

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    get_full_tus_products()

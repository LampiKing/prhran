"""
TUŠ 243 IZDELKOV - pravi selektorji
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_243_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ 243 IZDELKOV - PRAVI SELEKTORJI ===")

        # Odpri kategorije
        page.goto("https://hitrinakup.com/kategorije")
        page.wait_for_timeout(5000)

        # Klikni prvo kategorijo
        try:
            categories = page.query_selector_all("img[src*='kategorija_']")
            if categories:
                categories[0].click()
                print("Kliknil kategorijo")
                page.wait_for_timeout(5000)
        except Exception as e:
            print(f"Napaka: {e}")
            browser.close()
            return

        # Poberi vse izdelke z [class*='item'] - nasel je 243
        products = page.query_selector_all("[class*='item']")
        print(f"Najdenih {len(products)} item-ov")

        found_count = 0
        akcije_count = 0

        for i, product in enumerate(products[:30]):  # samo prvih 30
            try:
                # DOBI CEL HTML od producta
                product_html = product.inner_html()
                product_text = product.text_content() or ""

                # POIŠČI SLIKO
                img = product.query_selector("img")
                slika = ""
                if img:
                    src = img.get_attribute("src") or ""
                    if src and not src.startswith("data:"):
                        if src.startswith("/"):
                            slika = "https://hitrinakup.com" + src
                        else:
                            slika = src

                # POIŠČI IME - v HTML tagih
                name = ""
                # Isci h1, h2, h3 ali div z classom ki vsebuje 'name' ali 'title'
                name_selectors = [
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "div[class*='name']",
                    "div[class*='title']",
                    "span[class*='name']",
                ]

                for ns in name_selectors:
                    name_el = product.query_selector(ns)
                    if name_el:
                        name_text = name_el.text_content() or ""
                        if name_text.strip() and len(name_text.strip()) > 3:
                            name = name_text.strip()
                            break

                # Če ni našel ime, poišči v textu
                if not name:
                    lines = [
                        line.strip()
                        for line in product_text.split("\n")
                        if line.strip()
                    ]
                    for line in lines:
                        if len(line) > 3 and not any(
                            char.isdigit() for char in line[:10]
                        ):
                            name = line
                            break

                # POIŠČI CENE
                prices = re.findall(r"\d+[\.,]?\d*\s*(?:€|EUR)?", product_text)
                redna_cena = 0
                akcijska_cena = 0

                if len(prices) >= 2:
                    price_numbers = []
                    for price in prices:
                        num_match = re.search(r"(\d+[\.,]?\d*)", price)
                        if num_match:
                            price_numbers.append(
                                float(num_match.group(1).replace(",", "."))
                            )

                    if price_numbers:
                        redna_cena = max(price_numbers)
                        akcijska_cena = min(price_numbers)
                elif len(prices) == 1:
                    num_match = re.search(r"(\d+[\.,]?\d*)", prices[0])
                    if num_match:
                        redna_cena = float(num_match.group(1).replace(",", "."))

                # POIŠČI ENOTO
                unit = ""
                unit_patterns = [
                    r"(\d+)\s*(kg|g|l|ml|kos|kom|paket|pack)",
                    r"(\d+g|\d+kg|\d+l|\d+ml|\d+kos|\d+kom|\d+paket|\d+pack)",
                ]

                for pattern in unit_patterns:
                    match = re.search(pattern, product_text, re.IGNORECASE)
                    if match:
                        unit = match.group(0)
                        break

                # Dodaj v seznam
                if name and redna_cena > 0:
                    found_count += 1

                    # AKCIJA?
                    is_akcija = akcijska_cena > 0 and akcijska_cena != redna_cena
                    if is_akcija:
                        akcije_count += 1

                    print(f"\n[{found_count}] {name[:60]}...")
                    print(f"   Cena: {redna_cena}€", end="")
                    if is_akcija:
                        prihranek = redna_cena - akcijska_cena
                        odstotek = (prihranek / redna_cena) * 100
                        print(
                            f" → {akcijska_cena}€ (SALE -{prihranek:.2f}€, -{odstotek:.0f}%) 🔥"
                        )
                    else:
                        print()

                    if unit:
                        print(f"   Enota: {unit}")
                    if slika:
                        print(f"   Slika: {slika[:50]}...")

            except Exception as e:
                print(f"    Napaka produkt {i + 1}: {e}")
                continue

        print(f"\n" + "=" * 50)
        print(f"SKUPAJ: {found_count} izdelkov")
        print(f"AKCIJE: {akcije_count} izdelkov")
        print(f"NAVIDNI: {found_count - akcije_count} izdelkov")
        print("=" * 50)

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_243_products()

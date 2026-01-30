"""
TUŠ TEST - 2 IZDELKA (1 akcija, 1 navaden) - čista verzija
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_test_2_clean():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ TEST - 2 IZDELKA ===")

        # Testiram podkategorijo ki ima akcije
        page.goto("https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava")
        page.wait_for_timeout(5000)

        # Scroll
        for i in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

        # Poberi izdelke
        products = page.query_selector_all("[class*='item']")
        print(f"Najdenih {len(products)} elementov")

        found_normal = None
        found_akcija = None

        for i, product in enumerate(products[:20]):  # prvih 20
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

                # Če ni imena, poišči v textu
                if not name:
                    text = product.text_content() or ""
                    lines = text.split("\n")
                    for line in lines:
                        line = line.strip()
                        if len(line) > 3 and not any(
                            char.isdigit() for char in line[:15]
                        ):
                            name = line
                            break

                # CENE
                text = product.text_content() or ""
                price_matches = re.findall(r"\d+[\.,]?\d*", text)

                redna_cena = 0
                akcijska_cena = 0

                if price_matches:
                    prices_num = []
                    for match in price_matches:
                        try:
                            prices_num.append(float(match.replace(",", ".")))
                        except:
                            continue

                    if len(prices_num) >= 2:
                        redna_cena = max(prices_num)
                        akcijska_cena = min(prices_num)
                    elif len(prices_num) == 1:
                        redna_cena = prices_num[0]

                # SLIKA
                img = product.query_selector("img")
                slika = "DA" if img else "NE"

                # Preveri če smo našli izdelek
                if name and redna_cena > 0:
                    is_akcija = akcijska_cena > 0 and akcijska_cena != redna_cena

                    if is_akcija and not found_akcija:
                        found_akcija = {
                            "ime": name,
                            "redna_cena": redna_cena,
                            "akcijska_cena": akcijska_cena,
                            "slika": slika,
                            "kategorija": "Shramba",
                        }
                        print(f"\nAKCIJA: {name[:50]}...")
                        print(f"   {redna_cena} EUR -> {akcijska_cena} EUR")
                        print(f"   Pohritek: {redna_cena - akcijska_cena:.2f} EUR")

                    elif not is_akcija and not found_normal:
                        found_normal = {
                            "ime": name,
                            "redna_cena": redna_cena,
                            "akcijska_cena": 0,
                            "slika": slika,
                            "kategorija": "Shramba",
                        }
                        print(f"\nNAVDEN: {name[:50]}...")
                        print(f"   Cena: {redna_cena} EUR")

                    # Če imamo oba, končaj
                    if found_normal and found_akcija:
                        break

            except Exception as e:
                continue

        # Prikaži rezultate
        print(f"\n" + "=" * 50)
        print(f"TUŠ REZULTATI:")
        print("=" * 50)

        if found_akcija:
            print(f"YES Akcijski izdelek: {found_akcija['ime'][:40]}...")
            print(
                f"   {found_akcija['redna_cena']} EUR -> {found_akcija['akcijska_cena']} EUR"
            )

        if found_normal:
            print(f"YES Navaden izdelek: {found_normal['ime'][:40]}...")
            print(f"   Cena: {found_normal['redna_cena']} EUR")

        print(f"\nStatus: {'POPNOM' if found_normal and found_akcija else 'NEDOKONC'}")

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_test_2_clean()

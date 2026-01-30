"""
TUŠ CENE POPRAVEK - samo prave cene €
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_fix_cene():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ POPRAVLJENE CENE ===")

        # Testiram na Sadje in zelenjava
        page.goto("https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava")
        page.wait_for_timeout(5000)

        # Scroll
        for i in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

        products = page.query_selector_all("[class*='item']")
        print(f"Najdenih {len(products)} elementov")

        for i, product in enumerate(products[:10]):  # prvih 10 za test
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

                # PRAVILNE CENE - samo z € znakom
                text = product.text_content() or ""

                # Išči samo cene z € znakom
                price_with_eur = re.findall(r"\d+[\.,]?\d*\s*€", text)

                redna_cena = 0
                akcijska_cena = 0

                if price_with_eur:
                    prices_num = []
                    for match in price_with_eur:
                        try:
                            price_num = float(
                                re.search(r"(\d+[\.,]?\d*)", match)
                                .group(1)
                                .replace(",", ".")
                            )
                            # Filtriraj nerealne cene (nad 100€ za sadje/zelenjavo)
                            if price_num < 100:  # samo normalne cene
                                prices_num.append(price_num)
                        except:
                            continue

                    if len(prices_num) >= 2:
                        redna_cena = max(prices_num)
                        akcijska_cena = min(prices_num)
                    elif len(prices_num) == 1:
                        redna_cena = prices_num[0]

                # Če ni našel z €, poizkusi še brez ampak preveri razumno vrednost
                if redna_cena == 0:
                    # Išči cene ki so z besedami "cena", "eur", "eur/kos" itd.
                    reasonable_prices = []
                    all_numbers = re.findall(r"\d+[\.,]?\d*", text)

                    for num in all_numbers:
                        try:
                            price_val = float(num.replace(",", "."))
                            # Samo razumne cene za živila (0.1€ - 100€)
                            if 0.1 <= price_val <= 100:
                                # Preveri da ni količina (400g, 1kg) po kontekstu
                                context = text[
                                    text.find(num) - 10 : text.find(num) + 10
                                ]
                                if not any(
                                    x in context.lower()
                                    for x in ["g", "kg", "l", "ml", "kos"]
                                ):
                                    reasonable_prices.append(price_val)
                        except:
                            continue

                    if reasonable_prices:
                        if len(reasonable_prices) >= 2:
                            redna_cena = max(reasonable_prices)
                            akcijska_cena = min(reasonable_prices)
                        else:
                            redna_cena = reasonable_prices[0]

                # Prikaži
                if name:
                    print(f"\n[{i + 1}] {name[:50]}...")
                    if redna_cena > 0:
                        if akcijska_cena > 0 and akcijska_cena != redna_cena:
                            prihranek = redna_cena - akcijska_cena
                            odstotek = (prihranek / redna_cena) * 100
                            print(
                                f"   CENA: {redna_cena}€ -> {akcijska_cena}€ (AKCIJA -{prihranek:.2f}€, -{odstotek:.0f}%)"
                            )
                        else:
                            print(f"   CENA: {redna_cena}€")
                    else:
                        print(f"   CENA: Ni najdena")

            except Exception as e:
                continue

        print(f"\n--- TEST KONČAN ---")
        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_fix_cene()

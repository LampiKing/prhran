"""
TUŠ PRAVILNE CENE - 2,99€ format
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_correct_cene():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ PRAVILNE CENE ===")

        page.goto("https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava/Zelenjava")
        page.wait_for_timeout(5000)

        products = page.query_selector_all("[class*='item']")
        print(f"Najdenih {len(products)} elementov")

        # Testiram prvih 5
        for i, product in enumerate(products[:5]):
            try:
                text = product.text_content() or ""

                # Poišči IME
                name = ""
                lines = text.split("\n")
                for line in lines:
                    line = line.strip()
                    if (
                        len(line) > 3
                        and "g" in line
                        and not any(char.isdigit() for char in line[:20])
                    ):
                        name = line
                        break

                # Poišči CENE v formatu kot je v textu
                # Format: "kos2,99€€7,48€€/kgBrokoli in cvetača, pak., 400 g"

                # Metoda 1: X,XX€ pattern
                price_matches = re.findall(r"\d+,\d+\s*€", text)
                redna_cena = 0
                akcijska_cena = 0

                if price_matches:
                    prices_num = []
                    for match in price_matches:
                        try:
                            price = float(
                                match.replace(",", ".").replace("€", "").strip()
                            )
                            # Filter za normalne cene (0.1 - 50)
                            if 0.1 <= price <= 50:
                                prices_num.append(price)
                        except:
                            continue

                    if len(prices_num) >= 2:
                        redna_cena = max(prices_num)
                        akcijska_cena = min(prices_num)
                    elif len(prices_num) == 1:
                        redna_cena = prices_num[0]

                # Metoda 2: €/kg pattern - ignore
                if redna_cena == 0:
                    # Išči cene ki niso €/kg
                    all_eur = re.findall(r"(\d+,\d+)\s*€(?!.*(?:/kg))", text)
                    prices_num = []
                    for match in all_eur:
                        try:
                            price = float(match.replace(",", "."))
                            if 0.1 <= price <= 50:
                                prices_num.append(price)
                        except:
                            continue

                    if prices_num:
                        redna_cena = prices_num[0]
                        if len(prices_num) > 1:
                            akcijska_cena = min(prices_num)

                print(f"\n[{i + 1}] {name[:50]}...")
                print(f"  TEXT: {text[:100]}...")

                if redna_cena > 0:
                    if akcijska_cena > 0 and akcijska_cena != redna_cena:
                        prihranek = redna_cena - akcijska_cena
                        odstotek = (prihranek / redna_cena) * 100
                        print(
                            f"  CENA: {redna_cena}€ -> {akcijska_cena}€ (AKCIJA -{prihranek:.2f}€, -{odstotek:.0f}%)"
                        )
                    else:
                        print(f"  CENA: {redna_cena}€")
                else:
                    print(f"  CENA: Ni najdena")

            except Exception as e:
                print(f"Napaka: {e}")

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_correct_cene()

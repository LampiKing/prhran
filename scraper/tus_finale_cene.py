"""
TUŠ FINALE - ignoriraj €/kg bolj natančno
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_finale_cene():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ FINALE - prava cena paketa ===")

        page.goto("https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava/Zelenjava")
        page.wait_for_timeout(5000)

        products = page.query_selector_all("[class*='item']")
        print(f"Najdenih {len(products)} elementov")

        for i, product in enumerate(products[:5]):
            try:
                text = product.text_content() or ""

                # IME
                name = ""
                lines = text.split("\n")
                for line in lines:
                    line = line.strip()
                    if (
                        len(line) > 3
                        and "g" in line
                        and not any(char.isdigit() for char in line[:30])
                    ):
                        name = line
                        break

                # PRAVILNA LOGIKA:
                # 1. Poišči cene z njihovim kontekstom
                price_with_context = re.findall(r"(\d+,\d+\s*€[^/]{0,20})", text)

                normal_prices = []
                redna_cena = 0
                akcijska_cena = 0

                # 2. Preveri vsako ceno
                for price_context in price_with_context:
                    price_match = re.search(r"(\d+,\d+)\s*€", price_context)
                    if price_match:
                        price = float(price_match.group(1).replace(",", "."))

                        # Preveri da ni €/kg
                        if (
                            "/kg" not in price_context.lower()
                            and "€/kg" not in price_context.lower()
                        ):
                            # Realne cene za živila
                            if 0.1 <= price <= 50:
                                normal_prices.append(price)

                # 3. Če ni našel, poizkusi drugače
                if not normal_prices:
                    # Išči samo prvo ceno pred €/kg
                    simple_matches = re.findall(r"(\d+,\d+)\s*€", text)
                    for price_str in simple_matches:
                        price = float(price_str.replace(",", "."))
                        # Preveri pozicijo
                        pos = text.find(price_str)
                        context_after = text[pos : pos + 20]

                        if (
                            "/kg" not in context_after.lower()
                            and "€/kg" not in context_after.lower()
                        ):
                            if 0.1 <= price <= 50:
                                normal_prices.append(price)

                # 4. Določi končne cene
                if normal_prices:
                    # Če je več cen, vzemi najnižjo kot normalno cena
                    redna_cena = min(normal_prices)

                    # Če je več kot 1 cena in so različne, je akcija
                    unique_prices = list(set(normal_prices))
                    if len(unique_prices) > 1:
                        akcijska_cena = min(unique_prices)
                        redna_cena = max(unique_prices)

                # ENOTA
                unit = ""
                unit_match = re.search(r"(\d+)\s*(g|kg)", text)
                if unit_match:
                    unit = unit_match.group(0)

                print(f"\n[{i + 1}] {name[:50]}...")
                print(f"  TEXT: {text}")
                print(f"  NORM CENE: {normal_prices}")

                if redna_cena > 0:
                    if akcijska_cena > 0 and akcijska_cena != redna_cena:
                        prihranek = redna_cena - akcijska_cena
                        odstotek = (prihranek / redna_cena) * 100
                        print(
                            f"  CENA: {redna_cena}€ -> {akcijska_cena}€ (AKCIJA -{prihranek:.2f}€, -{odstotek:.0f}%)"
                        )
                    else:
                        print(f"  CENA: {redna_cena}€ (normalna)")

                    if unit:
                        print(f"  Količina: {unit}")
                else:
                    print(f"  CENA: Ni najdena")

            except Exception as e:
                continue

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_finale_cene()

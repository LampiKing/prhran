"""
TUŠ PRAVILNA LOGIKA - ignoriraj €/kg
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_pravilna_logika():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ PRAVILNA LOGIKA - ignoriraj €/kg ===")

        page.goto("https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava/Zelenjava")
        page.wait_for_timeout(5000)

        products = page.query_selector_all("[class*='item']")
        print(f"Najdenih {len(products)} elementov")

        for i, product in enumerate(products[:5]):
            try:
                text = product.text_content() or ""

                # Poišči IME
                name = ""
                lines = text.split("\n")
                for line in lines:
                    line = line.strip()
                    # Poišči ime (brez števil, €/kg)
                    if (
                        len(line) > 3
                        and "g" in line
                        and not any(char.isdigit() for char in line[:30])
                    ):
                        name = line
                        break

                # PRAVILNA CENA LOGIKA:
                # 1. Poišči vse cene
                all_prices = re.findall(r"\d+,\d+\s*€", text)
                price_numbers = []

                for price_text in all_prices:
                    price_num = float(
                        price_text.replace(",", ".").replace("€", "").strip()
                    )
                    price_numbers.append(price_num)

                # 2. FILTRIRAJ: ignoriraj €/kg cene
                # €/kg cene so višje (običajno nad 5€ za sadje/zelenjavo)
                normal_prices = []
                for price in price_numbers:
                    # Če je cena med 0.1€ in 20€, je verjetno cena paketa
                    if 0.1 <= price <= 20:
                        # Preveri kontekst - če je blizu "/kg" jo ignoriraj
                        context = text[
                            text.find(str(price).replace(".", ",")) - 20 : text.find(
                                str(price).replace(".", ",")
                            )
                            + 20
                        ]
                        if "/kg" not in context.lower():
                            normal_prices.append(price)

                # 3. DOBI KONČNO CENO
                redna_cena = 0
                akcijska_cena = 0

                if normal_prices:
                    if len(normal_prices) >= 2:
                        redna_cena = max(normal_prices)
                        akcijska_cena = min(normal_prices)
                    else:
                        redna_cena = normal_prices[0]

                # ENOTA
                unit = ""
                unit_match = re.search(r"(\d+)\s*(g|kg)", text)
                if unit_match:
                    unit = unit_match.group(0)

                print(f"\n[{i + 1}] {name[:50]}...")
                print(f"  TEXT: {text[:80]}...")
                print(f"  VSE CENE: {price_numbers}")
                print(f"  NORMAL CENE: {normal_prices}")

                if redna_cena > 0:
                    if akcijska_cena > 0 and akcijska_cena != redna_cena:
                        prihranek = redna_cena - akcijska_cena
                        odstotek = (prihranek / redna_cena) * 100
                        print(
                            f"  CENA: {redna_cena}€ -> {akcijska_cena}€ (AKCIJA -{prihranek:.2f}€, -{odstotek:.0f}%)"
                        )
                    else:
                        print(f"  CENA: {redna_cena}€ (navadna)")

                    if unit:
                        print(f"  Količina: {unit}")
                else:
                    print(f"  CENA: Ni najdena")

            except Exception as e:
                continue

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_pravilna_logika()

"""
TUŠ TEST RAZLIČNI IZDELKI - en drug link
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_test_drugi_izdelki():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ TEST - RAZLIČNI IZDELKI ===")

        # Uporabim drug link - ne zelenjava
        page.goto(
            "https://hitrinakup.com/kategorije/Meso,%20delikatesa%20in%20ribe/Meso"
        )
        page.wait_for_timeout(5000)

        # Scroll
        for i in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

        products = page.query_selector_all("[class*='item']")
        print(f"Najdenih {len(products)} elementov")

        # Poberi prvih 5 različnih izdelkov
        for i, product in enumerate(products[:5]):
            try:
                text = product.text_content() or ""

                # IME
                name = ""
                lines = text.split("\n")
                for line in lines:
                    line = line.strip()
                    if len(line) > 3 and not any(char.isdigit() for char in line[:30]):
                        name = line
                        break

                # CENE
                price_matches = re.findall(r"(\d+,\d+\s*€)", text)
                prices_with_context = []

                for match in price_matches:
                    pos = text.find(match)
                    context = text[pos - 10 : pos + 30]

                    if "/kg" not in context.lower():
                        price_num = float(
                            match.replace(",", ".").replace("€", "").strip()
                        )
                        if 0.1 <= price_num <= 50:
                            prices_with_context.append(price_num)

                redna_cena = 0
                akcijska_cena = 0

                if prices_with_context:
                    if len(prices_with_context) >= 2:
                        redna_cena = max(prices_with_context)
                        akcijska_cena = min(prices_with_context)
                    else:
                        redna_cena = prices_with_context[0]

                # ENOTA
                unit = ""
                unit_match = re.search(r"(\d+)\s*(g|kg)", text)
                if unit_match:
                    unit = unit_match.group(0)

                # SLIKA
                img = product.query_selector("img")
                slika = "DA" if img else "NE"

                print(f"\n[{i + 1}] {name[:60]}...")
                print(f"  TEXT: {text[:100]}...")
                print(f"  CENE: {prices_with_context}")

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
                    if slika == "DA":
                        print(f"  Slika: DA")
                else:
                    print(f"  CENA: Ni najdena")

            except Exception as e:
                continue

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_test_drugi_izdelki()

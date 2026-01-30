"""
TUŠ HITRO - jogurti kjer so akcije
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_jogurti_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ JOGURTI - AKCIJE ===")

        page.goto(
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Jogurti"
        )
        page.wait_for_timeout(5000)

        # Scroll
        for i in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

        products = page.query_selector_all("[class*='item']")
        print(f"Najdenih {len(products)} elementov")

        # Poberi prvih 5
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
                prices = []

                for match in price_matches:
                    pos = text.find(match)
                    context = text[pos - 10 : pos + 30]

                    if "/kg" not in context.lower():
                        price_num = float(
                            match.replace(",", ".").replace("€", "").strip()
                        )
                        if 0.1 <= price_num <= 50:
                            prices.append(price_num)

                redna_cena = 0
                akcijska_cena = 0

                if prices:
                    if len(prices) >= 2:
                        redna_cena = max(prices)
                        akcijska_cena = min(prices)
                    else:
                        redna_cena = prices[0]

                print(f"\n[{i + 1}] {name[:50]}...")
                print(f"  TEXT: {text}")
                print(f"  CENE: {prices}")

                if redna_cena > 0:
                    if akcijska_cena > 0 and akcijska_cena != redna_cena:
                        print(f"  CENA: {redna_cena}€ -> {akcijska_cena}€ (AKCIJA!)")
                    else:
                        print(f"  CENA: {redna_cena}€ (normalna)")
                else:
                    print(f"  CENA: Ni najdena")

                # Če imamo eno akcijo, končaj
                if akcijska_cena > 0:
                    print(f"\nNAŠLI AKCIJO!")
                    break

            except Exception as e:
                continue

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_jogurti_test()

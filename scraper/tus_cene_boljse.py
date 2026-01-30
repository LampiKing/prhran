"""
TUŠ CENE - iskanje z "Cena:" oznako
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_cene_with_label():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print('=== TUŠ CENE Z "CENA:" OZNAKO ===')

        page.goto("https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava")
        page.wait_for_timeout(5000)

        # Scroll
        for i in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

        products = page.query_selector_all("[class*='item']")
        print(f"Najdenih {len(products)} elementov")

        for i, product in enumerate(products[:15]):  # prvih 15
            try:
                # Dobi cel HTML za boljše iskanje
                html = product.inner_html()
                text = product.text_content() or ""

                # IME - poišči v HTML ali text
                name = ""
                # Poišči v HTML-ju za h1-h4
                for tag in ["h1", "h2", "h3", "h4"]:
                    if f"<{tag}" in html:
                        name_match = re.search(
                            f"<{tag}[^>]*>([^<]+)</{tag}>", html, re.IGNORECASE
                        )
                        if name_match:
                            name = name_match.group(1).strip()
                            break

                # Če ni v HTML, poišči v textu
                if not name:
                    lines = text.split("\n")
                    for line in lines:
                        line = line.strip()
                        if (
                            len(line) > 3
                            and not any(char.isdigit() for char in line[:15])
                            and "kategorije" not in line.lower()
                        ):
                            name = line
                            break

                # CENE - iskanje z boljšimi filtri
                redna_cena = 0
                akcijska_cena = 0

                # Metoda 1: Poišči "Cena:" v textu
                cena_matches = re.findall(r"[Cc]ena[:\s]*\s*(\d+[\.,]?\d*)", text)
                if cena_matches:
                    for match in cena_matches:
                        try:
                            price = float(match.replace(",", "."))
                            if 0.1 <= price <= 50:  # realne cene za živila
                                if not redna_cena:
                                    redna_cena = price
                                elif price != redna_cena:
                                    akcijska_cena = min(price, redna_cena)
                                    redna_cena = max(price, redna_cena)
                        except:
                            continue

                # Metoda 2: Poišši cene v HTML-ju
                if redna_cena == 0:
                    # Išči cene v HTML div elementih z price classi
                    price_html_matches = re.findall(
                        r"<[^>]*[Pp]rice[^>]*>(\d+[\.,]?\d*)", html
                    )
                    if price_html_matches:
                        for match in price_html_matches:
                            try:
                                price = float(match.replace(",", "."))
                                if 0.1 <= price <= 50:
                                    if not redna_cena:
                                        redna_cena = price
                                    elif price != redna_cena:
                                        akcijska_cena = min(price, redna_cena)
                                        redna_cena = max(price, redna_cena)
                            except:
                                continue

                # Metoda 3: Poišči € blizu števil (brez g/kg)
                if redna_cena == 0:
                    eur_matches = re.findall(
                        r"(\d+[\.,]?\d*)\s*€(?!.*(?:kg|g|l|ml))", text
                    )
                    if eur_matches:
                        for match in eur_matches:
                            try:
                                price = float(match.replace(",", "."))
                                if 0.1 <= price <= 50:
                                    if not redna_cena:
                                        redna_cena = price
                                    elif price != redna_cena:
                                        akcijska_cena = min(price, redna_cena)
                                        redna_cena = max(price, redna_cena)
                            except:
                                continue

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
    tus_cene_with_label()

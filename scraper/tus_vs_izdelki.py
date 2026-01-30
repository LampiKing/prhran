"""
TUŠ ZELEN GUMB - Vsi izdelki iz kategorije
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_vs_izdelki():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ ZELEN GUMB - VSI IZDELKI ===")

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

        # Poišči "Vsi izdelki iz kategorije" gumb
        print("\nIskem 'Vsi izdelki iz kategorije' gumb...")

        # Različni možni gumbi
        button_selectors = [
            "button:has-text('Vsi izdelki iz kategorije')",
            "a:has-text('Vsi izdelki iz kategorije')",
            "button:has-text('Vsi izdelki')",
            "a:has-text('Vsi izdelki')",
            "[class*='all-products']",
            "[class*='see-all']",
            "button[class*='green']",
            "button[class*='primary']",
            ".btn-primary",
            "button",
        ]

        button_found = False
        for selector in button_selectors:
            try:
                buttons = page.query_selector_all(selector)
                if buttons:
                    print(f"Najdenih {len(buttons)} gumbov z: {selector}")

                    for i, btn in enumerate(buttons):
                        btn_text = btn.text_content() or ""
                        if "vsi izdelk" in btn_text.lower() or "vs" in btn_text.lower():
                            print(f"  Kliknil gumb: {btn_text.strip()}")
                            btn.click()
                            button_found = True
                            page.wait_for_timeout(5000)
                            break

                    if button_found:
                        break

            except Exception as e:
                continue

        if not button_found:
            print("Gumb ni najden, poizkusim scroll...")
            # Scroll navzdol da se more pojavit gumb
            for i in range(3):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(2000)

                # Ponovno poizkusi najti gumb
                for selector in button_selectors:
                    try:
                        buttons = page.query_selector_all(selector)
                        for btn in buttons:
                            btn_text = btn.text_content() or ""
                            if "vsi izdelk" in btn_text.lower():
                                print(f"Našel gumb po scrollu: {btn_text.strip()}")
                                btn.click()
                                button_found = True
                                page.wait_for_timeout(5000)
                                break
                        if button_found:
                            break
                    except:
                        continue
                if button_found:
                    break

        # Poberi vse izdelke
        print("\nScrapam izdelke...")

        # Naredi več scroll-ov za vse izdelke
        for i in range(10):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

        # Najdi vse izdelke
        products = []

        # Boljši selektorji za TUŠ Next.js
        product_selectors = [
            "[data-product]",
            "article[data-testid*='product']",
            "[class*='ProductCard']",
            "[class*='product-item']",
            ".product",
            "article",
            "[class*='item']",
        ]

        all_products = []
        for selector in product_selectors:
            try:
                products_found = page.query_selector_all(selector)
                if products_found:
                    print(f"Najdenih {len(products_found)} izdelkov z: {selector}")
                    all_products = products_found
                    break
            except:
                continue

        print(f"Processing {len(all_products)} products...")

        found_count = 0
        for i, product in enumerate(all_products[:20]):  # prvih 20 za test
            try:
                # Preberi cel text v produktu
                product_text = product.text_content() or ""

                # Poišči ime - prvi "useben" text
                name = ""
                if len(product_text.strip()) > 3:
                    lines = [
                        line.strip()
                        for line in product_text.split("\n")
                        if line.strip()
                    ]
                    if lines:
                        # Skip cene iščeš ime
                        for line in lines:
                            if (
                                not any(char.isdigit() for char in line)
                                and len(line) > 3
                            ):
                                name = line
                                break

                # Poišči cene v textu
                prices = re.findall(r"\d+[\.,]?\d*\s*(?:€|EUR)", product_text)
                redna_cena = 0
                akcijska_cena = 0

                if prices:
                    price_numbers = []
                    for price in prices:
                        num_match = re.search(r"(\d+[\.,]?\d*)", price)
                        if num_match:
                            price_numbers.append(
                                float(num_match.group(1).replace(",", "."))
                            )

                    if len(price_numbers) >= 2:
                        redna_cena = max(price_numbers)
                        akcijska_cena = min(price_numbers)
                    elif len(price_numbers) == 1:
                        redna_cena = price_numbers[0]

                # Slika
                img = product.query_selector("img")
                slika = ""
                if img:
                    src = img.get_attribute("src") or ""
                    if src and src.startswith("/"):
                        slika = "https://hitrinakup.com" + src
                    else:
                        slika = src

                # Shrani
                if name and (redna_cena > 0 or akcijska_cena > 0):
                    found_count += 1
                    print(f"\n[{found_count}] {name[:50]}...")
                    if redna_cena > 0:
                        print(f"   Redna: {redna_cena} EUR")
                    if akcijska_cena > 0 and akcijska_cena != redna_cena:
                        print(f"   Akcijska: {akcijska_cena} EUR (Pohritek!)")
                    if slika:
                        print(f"   Slika: {slika[:60]}...")

            except Exception as e:
                print(f"    Napaka produkt {i + 1}: {e}")
                continue

        print(f"\n=== REZULTAT ===")
        print(f"Skupaj najdenih: {found_count} izdelkov")

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_vs_izdelki()

"""
TUŠ TEST - samo 2 cene iz tvojih linkov
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_test_2cene():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ TEST 2 CENE ===")

        # Preberi tvoje linke
        with open(
            r"C:\Users\lampr\Desktop\TUŠ_KATEGORIJE.txt", "r", encoding="utf-8"
        ) as f:
            content = f.read().strip()

        urls = [url.strip() for url in content.split(",") if url.strip()]

        # Testiram samo prva 2 linka
        for i, url in enumerate(urls[:2]):
            print(f"\n--- Link {i + 1}: {url.split('/')[-1]} ---")

            try:
                page.goto(url)
                page.wait_for_timeout(4000)

                # Scroll
                for scroll in range(3):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(2000)

                products = page.query_selector_all("[class*='item']")
                print(f"Najdenih {len(products)} elementov")

                # Poberi samo prvih 5 izdelkov
                for j, product in enumerate(products[:5]):
                    try:
                        # IME
                        html = product.inner_html()
                        text = product.text_content() or ""

                        name = ""
                        for tag in ["h1", "h2", "h3", "h4"]:
                            match = re.search(
                                f"<{tag}[^>]*>([^<]+)</{tag}>", html, re.IGNORECASE
                            )
                            if match:
                                name = match.group(1).strip()
                                break

                        # CENA - Google extension logika
                        # Išči samo CENA: z realnimi vrednostmi
                        cena_text = text.replace(",", ".")

                        # Metoda 1: "Cena:" oznaka
                        cena_match = re.search(r"[Cc]ena[:\s]*(\d+\.?\d*)", cena_text)
                        if cena_match:
                            cena = float(cena_match.group(1))
                            if 0.1 <= cena <= 50:
                                print(f"  {j + 1}. {name[:40]}... - CENA: {cena} EUR")
                                continue

                        # Metoda 2: € znak brez g/kg/ml
                        eur_match = re.findall(
                            r"(\d+\.?\d*)\s*€(?!.*(?:kg|g|l|ml))", cena_text
                        )
                        for match in eur_match:
                            cena = float(match)
                            if 0.1 <= cena <= 50:
                                print(f"  {j + 1}. {name[:40]}... - CENA: {cena} EUR")
                                break
                        else:
                            print(f"  {j + 1}. {name[:40]}... - CENA: ni najdena")

                    except Exception as e:
                        continue

            except Exception as e:
                print(f"NAPAKA: {e}")

        print(f"\n--- KONEC ---")
        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_test_2cene()

"""
TUŠ FINALNA VERZIJA - tvoji linki, akcije, slike
"""

from playwright.sync_api import sync_playwright
import time
import re
import json


def tus_final_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ FINAL - tvoji linki + AKCIJE ===")

        # Preberi tvoje linke
        with open(
            r"C:\Users\lampr\Desktop\TUŠ_KATEGORIJE.txt", "r", encoding="utf-8"
        ) as f:
            content = f.read().strip()

        urls = [url.strip() for url in content.split(",") if url.strip()]
        print(f"Processing {len(urls)} tvojih linkov...")

        total_all = 0
        total_akcije = 0
        all_products = []

        for i, url in enumerate(urls):
            print(f"\n--- Link {i + 1}/{len(urls)} ---")

            try:
                page.goto(url)
                page.wait_for_timeout(4000)

                # Scroll za vse izdelke
                for scroll in range(5):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(2000)

                products = page.query_selector_all("[class*='item']")
                print(f"Najdenih {len(products)} elementov")

                cat_count = 0
                cat_akcije = 0

                for product in products:  # VSE izdelke
                    try:
                        text = product.text_content() or ""

                        # IME
                        name = ""
                        lines = text.split("\n")
                        for line in lines:
                            line = line.strip()
                            if len(line) > 3 and not any(
                                char.isdigit() for char in line[:30]
                            ):
                                name = line
                                break

                        # CENE - finalna logika
                        # Poišči vse cene X,XX€
                        price_matches = re.findall(r"(\d+,\d+\s*€)", text)
                        prices_with_context = []

                        for match in price_matches:
                            # Preveri kontekst da ni €/kg
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
                                # Akcija: dve ceni
                                redna_cena = max(prices_with_context)
                                akcijska_cena = min(prices_with_context)
                            else:
                                # Normalna cena: ena cena
                                redna_cena = prices_with_context[0]

                        # ENOTA
                        unit = ""
                        unit_match = re.search(r"(\d+)\s*(g|kg|ml|l)", text)
                        if unit_match:
                            unit = unit_match.group(0)

                        # SLIKA
                        img = product.query_selector("img")
                        slika = ""
                        if img:
                            src = img.get_attribute("src") or ""
                            if src and not src.startswith("data:"):
                                if src.startswith("/"):
                                    slika = "https://hitrinakup.com" + src
                                else:
                                    slika = src

                        # Shrani produkt
                        if name and redna_cena > 0:
                            cat_count += 1
                            total_all += 1

                            is_akcija = (
                                akcijska_cena > 0 and akcijska_cena != redna_cena
                            )
                            if is_akcija:
                                cat_akcije += 1
                                total_akcije += 1

                            product_data = {
                                "ime": name,
                                "trgovina": "Tuš",
                                "redna_cena": redna_cena,
                                "akcijska_cena": akcijska_cena if is_akcija else 0,
                                "enota": unit,
                                "slika": slika,
                                "kategorija": url.split("/")[-1]
                                if "/" in url
                                else "Unknown",
                                "url": url,
                            }

                            all_products.append(product_data)

                    except Exception as e:
                        continue

                print(f"KONČANO: {cat_count} izdelkov ({cat_akcije} akcij)")

            except Exception as e:
                print(f"NAPAKA: {e}")

        # Shrani v JSON
        with open(
            r"C:\Users\lampr\Desktop\PrHran\scraper\tus_final_results.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(all_products, f, ensure_ascii=False, indent=2)

        # Končni rezultati
        print(f"\n" + "=" * 60)
        print(f"TUŠ FINAL REZULTATI:")
        print(f"Kategorij: {len(urls)}")
        print(f"Vseh izdelkov: {total_all}")
        print(f"Akcijskih: {total_akcije}")
        print(f"Navadnih: {total_all - total_akcije}")
        print(
            f"JSON: C:\\Users\\lampr\\Desktop\\PrHran\\scraper\\tus_final_results.json"
        )
        print("=" * 60)

        return all_products


if __name__ == "__main__":
    results = tus_final_all()
    print(f"\nKONČANO! {len(results)} TUŠ izdelkov shranjenih!")

"""
TUŠ ALL CATEGORIES - samo tvoji linki iz datoteke
"""

from playwright.sync_api import sync_playwright
import time
import re
import json


def tus_final_from_file():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ SAMO TVOJI LINKI ===")

        # Preberi TOČNO tvoje linke iz datoteke
        with open(
            r"C:\Users\lampr\Desktop\TUŠ_KATEGORIJE.txt", "r", encoding="utf-8"
        ) as f:
            content = f.read().strip()

        # Razdeli po "," ker so tako ločeni
        urls = [url.strip() for url in content.split(",") if url.strip()]

        print(f"Najdenih {len(urls)} tvojih TUŠ linkov:")
        for i, url in enumerate(urls):
            print(f"  [{i + 1}] {url}")

        total_all = 0
        total_akcije = 0
        all_products = []

        for i, url in enumerate(urls):
            print(f"\n--- Tvoj link {i + 1}/{len(urls)} ---")
            print(f"URL: {url}")

            try:
                page.goto(url)
                page.wait_for_timeout(4000)

                # Scroll 8x da se naloži vse
                for scroll in range(8):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(2000)

                # Poberi vse izdelke
                products = page.query_selector_all("[class*='item']")
                print(f"Najdenih {len(products)} elementov")

                cat_count = 0
                cat_akcije = 0

                for j, product in enumerate(products):  # VSE izdelke
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

                        # CENE
                        text = product.text_content() or ""
                        price_matches = re.findall(r"\d+[\.,]?\d*", text)

                        redna_cena = 0
                        akcijska_cena = 0

                        if price_matches:
                            prices_num = []
                            for match in price_matches:
                                try:
                                    prices_num.append(float(match.replace(",", ".")))
                                except:
                                    continue

                            if len(prices_num) >= 2:
                                redna_cena = max(prices_num)
                                akcijska_cena = min(prices_num)
                            elif len(prices_num) == 1:
                                redna_cena = prices_num[0]

                        # ENOTA
                        unit = ""
                        unit_match = re.search(
                            r"(\d+)\s*(kg|g|l|ml|kos|kom)", text, re.IGNORECASE
                        )
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

        # Shrani vse produkte v JSON
        with open(
            r"C:\Users\lampr\Desktop\PrHran\scraper\tus_tvoji_linki.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(all_products, f, ensure_ascii=False, indent=2)

        # Končni rezultati
        print(f"\n" + "=" * 60)
        print(f"TUŠ TVOJI LINKI - KONEČNI REZULTATI:")
        print(f"Tvojih linkov: {len(urls)}")
        print(f"Vseh izdelkov: {total_all}")
        print(f"Akcijskih: {total_akcije}")
        print(f"Navadnih: {total_all - total_akcije}")
        print(
            f"JSON shranjen: C:\\Users\\lampr\\Desktop\\PrHran\\scraper\\tus_tvoji_linki.json"
        )
        print("=" * 60)

        return all_products


if __name__ == "__main__":
    results = tus_final_from_file()
    print(f"\nKončano! Pobranih {len(results)} TUŠ izdelkov!")

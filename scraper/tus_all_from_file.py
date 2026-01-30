"""
TUŠ ALL CATEGORIES - iz tvoje datoteke
"""

from playwright.sync_api import sync_playwright
import time
import re
import json


def tus_all_categories_from_file():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ VSE KATEGORIJE IZ DATOTEKE ===")

        # VSE TUŠ KATEGORIJE - direkten seznam
        urls = [
            "https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava/Zelenjava",
            "https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava/Pripravljene%20jedi",
            "https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava/Sadje",
            "https://hitrinakup.com/kategorije/Meso,%20delikatesa%20in%20ribe/Hlajene%20specialitete%20in%20solate",
            "https://hitrinakup.com/kategorije/Meso,%20delikatesa%20in%20ribe/Ribe",
            "https://hitrinakup.com/kategorije/Meso,%20delikatesa%20in%20ribe/Delikatesa",
            "https://hitrinakup.com/kategorije/Meso,%20delikatesa%20in%20ribe/Pripravljene%20jedi",
            "https://hitrinakup.com/kategorije/Meso,%20delikatesa%20in%20ribe/Sendvi%C4%8Di",
            "https://hitrinakup.com/kategorije/Meso,%20delikatesa%20in%20ribe/Meso",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Kefirji%20in%20sirotke",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Kislo%20mleko",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Smetane",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Jajca",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Siri",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Skute",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Masla",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Deserti",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Namazi",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Smutiji",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Jogurti",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Mleko",
            "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki/Margarine%20in%20masti",
            "https://hitrinakup.com/kategorije/Kruh%20in%20pekovski%20izdelki/Pekovsko%20pecivo",
            "https://hitrinakup.com/kategorije/Kruh%20in%20pekovski%20izdelki/Testo%20in%20mesi",
        ]

        print(f"Najdenih {len(urls)} TUŠ kategorij")

        total_all = 0
        total_akcije = 0
        all_products = []

        for i, url in enumerate(urls):
            print(f"\n--- Kategorija {i + 1}/{len(urls)} ---")
            print(f"URL: {url}")

            try:
                page.goto(url)
                page.wait_for_timeout(3000)

                # Scroll da se naloži vse
                for scroll in range(8):  # 8 scrollov za vse izdelke
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
            r"C:\Users\lampr\Desktop\PrHran\scraper\tus_all_products.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(all_products, f, ensure_ascii=False, indent=2)

        # Končni rezultati
        print(f"\n" + "=" * 60)
        print(f"TUŠ SKUPNI REZULTATI:")
        print(f"Kategorij: {len(urls)}")
        print(f"Vseh izdelkov: {total_all}")
        print(f"Akcijskih: {total_akcije}")
        print(f"Navadnih: {total_all - total_akcije}")
        print(
            f"JSON shranjen: C:\\Users\\lampr\\Desktop\\PrHran\\scraper\\tus_all_products.json"
        )
        print("=" * 60)

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_all_categories_from_file()

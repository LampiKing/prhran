"""
TUŠ AVTOMATSKI LOOP - vse kategorije
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_all_categories():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ VSE KATEGORIJE AVTOMATSKO ===")

        # Vse TUŠ kategorije URL-ji (ki jih poznam)
        categories = [
            (
                "Sadje in zelenjava",
                "https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava",
            ),
            (
                "Meso in ribe",
                "https://hitrinakup.com/kategorije/Meso%2C%20delikatesa%20in%20ribe",
            ),
            (
                "Mlečni izdelki",
                "https://hitrinakup.com/kategorije/Hlajeni%20in%20mle%C4%8Dni%20izdelki",
            ),
            (
                "Pekovski izdelki",
                "https://hitrinakup.com/kategorije/Pekovski%20izdelki",
            ),
            ("Shramba", "https://hitrinakup.com/kategorije/Shramba"),
            ("Pijače", "https://hitrinakup.com/kategorije/Pija%C4%8De"),
            (
                "Sladko in slano",
                "https://hitrinakup.com/kategorije/Sladko%20in%20slano",
            ),
            ("Kozmetika", "https://hitrinakup.com/kategorije/Kozmetika"),
            (
                "Hišni ljubljenčki",
                "https://hitrinakup.com/kategorije/Hi%C5%A1ni%20ljubljen%C4%8Dki",
            ),
            ("Otroški svet", "https://hitrinakup.com/kategorije/Otro%C5%A1ki%20svet"),
        ]

        total_all_products = 0
        total_akcije = 0

        for cat_name, cat_url in categories:
            try:
                print(f"\n=== {cat_name.upper()} ===")
                page.goto(cat_url)
                page.wait_for_timeout(3000)

                # Počakaj da se naložijo izdelki
                page.wait_for_timeout(2000)

                # Scroll za vse izdelke (hitro)
                for i in range(3):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(1000)

                # Poberi izdelke
                products = page.query_selector_all("[class*='item']")
                print(f"Najdenih {len(products)} item-ov")

                cat_products = 0
                cat_akcije = 0

                # Poberi prvih 10 izdelkov iz vsake kategorije za demo
                for i, product in enumerate(products[:10]):
                    try:
                        # IME
                        name = ""
                        name_selectors = ["h1", "h2", "h3", "h4", "[class*='name']"]
                        for ns in name_selectors:
                            name_el = product.query_selector(ns)
                            if name_el:
                                name_text = name_el.text_content() or ""
                                if name_text.strip():
                                    name = name_text.strip()
                                    break

                        # Če ni našel, poišči v textu
                        if not name:
                            text = product.text_content() or ""
                            lines = text.split("\n")
                            for line in lines:
                                line = line.strip()
                                if len(line) > 3 and not any(
                                    char.isdigit() for char in line[:10]
                                ):
                                    name = line
                                    break

                        # CENE
                        text = product.text_content() or ""
                        price_matches = re.findall(r"\d+[\.,]?\d*", text)

                        redna_cena = 0
                        akcijska_cena = 0

                        if price_matches:
                            prices_num = [
                                float(p.replace(",", ".")) for p in price_matches
                            ]
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
                        slika = "DA" if img else "NE"

                        # Dodaj v števce
                        if name and redna_cena > 0:
                            cat_products += 1
                            total_all_products += 1

                            is_akcija = (
                                akcijska_cena > 0 and akcijska_cena != redna_cena
                            )
                            if is_akcija:
                                cat_akcije += 1
                                total_akcije += 1

                            print(
                                f"  {cat_products}. {name[:40]}... - {redna_cena}€ {'(AKC!)' if is_akcija else ''}"
                            )

                    except Exception as e:
                        continue

                print(f"→ {cat_name}: {cat_products} izdelkov ({cat_akcije} akcij)")

            except Exception as e:
                print(f"→ {cat_name}: NAPAKA ({e})")
                continue

        print(f"\n" + "=" * 50)
        print(f"TUŠ SKUPNI REZULTATI:")
        print(f"VSEH KATEGORIJ: {len(categories)}")
        print(f"VSEH IZDELKOV: {total_all_products}")
        print(f"AKCIJSKIH IZDELKOV: {total_akcije}")
        print(
            f"POVPREČE NA KATEGORIJO: {total_all_products / len(categories):.0f} izdelkov"
        )
        print("=" * 50)

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_all_categories()

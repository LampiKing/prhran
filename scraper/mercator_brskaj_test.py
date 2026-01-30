"""
MERCATOR SCRAPER - brskaj z Google Extension logiko
"""

from playwright.sync_api import sync_playwright
import time
import re
import json


def mercator_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== MERCATOR - brskaj ===")

        # Odpri brskaj stran
        page.goto("https://mercatoronline.si/brskaj")
        page.wait_for_timeout(5000)

        # Sprejmi cookies če je potrebno
        try:
            page.click('button:has-text("Sprejmi")', timeout=3000)
        except:
            pass

        # Infinite scroll da naloži vse izdelke
        print("Infinite scroll za vse izdelke...")
        for i in range(20):  # 20 scroll-ov za vse
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

            # Preveri če se je content spremenil
            if i % 5 == 0:
                print(f"Scroll {i + 1}/20...")

        # Poberi vse izdelke
        print("\nScrapam izdelke...")

        # MERCATOR product selektorji
        product_selectors = [
            "[class*='product']",
            "[class*='item']",
            "[data-product]",
            "article",
            ".grid-item",
        ]

        all_products = []
        for selector in product_selectors:
            products = page.query_selector_all(selector)
            if products:
                print(f"Najdenih {len(products)} izdelkov z: {selector}")
                all_products = products
                break

        found_products = []

        # Poberi prvih 15 izdelkov za test
        for i, product in enumerate(all_products[:15]):
            try:
                text = product.text_content() or ""
                html = product.inner_html()

                # IME
                name = ""
                # Poišči v HTML h1-h4
                for tag in ["h1", "h2", "h3", "h4"]:
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
                        if len(line) > 3 and not any(
                            char.isdigit() for char in line[:20]
                        ):
                            if not any(
                                x in line.lower()
                                for x in ["eur", "€", "%", "pc", "kos"]
                            ):
                                name = line
                                break

                # MERCATOR CENA LOGIKA (Google Extension style)
                # Primer: "0,89 €0,63 €"
                # Primer: "1,69 € 1,29 €"
                # Primer: "2,99 €"

                # Metoda 1: Poišči vse X,XX €
                price_matches = re.findall(r"(\d+,\d+)\s*€", text)
                prices = []

                for match in price_matches:
                    price_num = float(match.replace(",", "."))
                    # Filter za realne cene (0.1 - 100)
                    if 0.1 <= price_num <= 100:
                        # Preveri kontekst da ni cena/liter
                        pos = text.find(match)
                        context_after = text[pos : pos + 20]
                        if (
                            "/l" not in context_after.lower()
                            and "/kg" not in context_after.lower()
                        ):
                            prices.append(price_num)

                redna_cena = 0
                akcijska_cena = 0

                if prices:
                    if len(prices) >= 2:
                        # Akcija: dve ceni
                        redna_cena = max(prices)
                        akcijska_cena = min(prices)
                    else:
                        # Normalna: ena cena
                        redna_cena = prices[0]

                # ENOTA
                unit = ""
                unit_patterns = [
                    r"(\d+)\s*l",
                    r"(\d+)\s*kg",
                    r"(\d+)\s*g",
                    r"(\d+)\s*ml",
                ]

                for pattern in unit_patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        unit = match.group(0)
                        break

                # POPUST %
                popust = 0
                popust_match = re.search(r"-(\d+)%", text)
                if popust_match:
                    popust = int(popust_match.group(1))

                # SLIKA
                img = product.query_selector("img")
                slika = ""
                if img:
                    src = img.get_attribute("src") or ""
                    if src and not src.startswith("data:"):
                        if src.startswith("/"):
                            slika = "https://mercatoronline.si" + src
                        else:
                            slika = src

                # Shrani produkt
                if name and redna_cena > 0:
                    is_akcija = akcijska_cena > 0 and akcijska_cena != redna_cena

                    product_data = {
                        "ime": name,
                        "trgovina": "Mercator",
                        "redna_cena": redna_cena,
                        "akcijska_cena": akcijska_cena if is_akcija else 0,
                        "enota": unit,
                        "slika": slika,
                        "popust": popust,
                        "kategorija": "brskaj",
                        "url": page.url,
                    }

                    found_products.append(product_data)

                    # Prikaži
                    print(f"\n[{len(found_products)}] {name[:50]}...")
                    if is_akcija:
                        prihranek = redna_cena - akcijska_cena
                        odstotek = (prihranek / redna_cena) * 100
                        print(
                            f"  CENA: {redna_cena}€ -> {akcijska_cena}€ (AKCIJA -{prihranek:.2f}€, -{odstotek:.0f}%)"
                        )
                        if popust > 0:
                            print(f"  POPUST: -{popust}%")
                    else:
                        print(f"  CENA: {redna_cena}€")

                    if unit:
                        print(f"  Enota: {unit}")
                    if slika:
                        print(f"  Slika: DA")

            except Exception as e:
                continue

        # Shrani v JSON
        with open(
            r"C:\Users\lampr\Desktop\PrHran\scraper\mercator_test.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(found_products, f, ensure_ascii=False, indent=2)

        print(f"\n" + "=" * 50)
        print(f"MERCATOR REZULTATI:")
        print(f"Skupaj: {len(found_products)} izdelkov")
        akcije = [p for p in found_products if p.get("akcijska_cena", 0) > 0]
        print(f"Akcijskih: {len(akcije)}")
        print(f"Navadnih: {len(found_products) - len(akcije)}")
        print(
            f"JSON shranjen: C:\\Users\\lampr\\Desktop\\PrHran\\scraper\\mercator_test.json"
        )
        print("=" * 50)

        return found_products


if __name__ == "__main__":
    results = mercator_scraper()
    print(f"\nMERCATOR TEST KONČAN! {len(results)} izdelkov")

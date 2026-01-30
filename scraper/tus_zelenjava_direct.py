"""
TUŠ DIREKT LINK - Zelenjava
https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava/Zelenjava
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_zelenjava_direct():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ DIREKT - ZELENJAVA ===")

        # Odpri direkt link
        page.goto("https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava/Zelenjava")
        page.wait_for_timeout(5000)

        print(f"Page title: {page.title()}")
        print(f"Current URL: {page.url}")

        # Počakaj da se naložijo vsi izdelki
        print("Čakam na izdelke...")
        page.wait_for_timeout(3000)

        # Scroll za vse izdelke
        for i in range(5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

        # Poberi vse izdelke
        products = page.query_selector_all("[class*='item']")
        print(f"Najdenih {len(products)} izdelkov")

        found_count = 0
        akcije = 0

        for i, product in enumerate(products[:20]):  # prvih 20 za demo
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
                price_matches = re.findall(r"\d+[\.,]?\d*\s*(?:€|EUR)?", text)

                redna_cena = 0
                akcijska_cena = 0

                if price_matches:
                    numbers = []
                    for match in price_matches:
                        num = re.search(r"(\d+[\.,]?\d*)", match)
                        if num:
                            numbers.append(float(num.group(1).replace(",", ".")))

                    if len(numbers) >= 2:
                        redna_cena = max(numbers)
                        akcijska_cena = min(numbers)
                    elif len(numbers) == 1:
                        redna_cena = numbers[0]

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

                # ENOTA
                unit = ""
                unit_match = re.search(
                    r"(\d+)\s*(kg|g|l|ml|kos|kom)", text, re.IGNORECASE
                )
                if unit_match:
                    unit = unit_match.group(0)

                # Prikaži
                if name and redna_cena > 0:
                    found_count += 1

                    is_akcija = akcijska_cena > 0 and akcijska_cena != redna_cena
                    if is_akcija:
                        akcije += 1

                    print(f"\n[{found_count}] {name[:50]}...")
                    if is_akcija:
                        prihranek = redna_cena - akcijska_cena
                        odstotek = (prihranek / redna_cena) * 100
                        print(
                            f"   {redna_cena}€ -> {akcijska_cena}€ (AKCIJA -{prihranek:.2f}€, -{odstotek:.0f}%)"
                        )
                    else:
                        print(f"   Cena: {redna_cena}€")

                    if unit:
                        print(f"   Enota: {unit}")
                    if slika:
                        print(f"   Slika: DA")

            except Exception as e:
                continue

        print(f"\n" + "=" * 40)
        print(f"ZELENJAVA REZULTATI:")
        print(f"Skupaj: {found_count} izdelkov")
        print(f"Akcijskih: {akcije}")
        print(f"Navadnih: {found_count - akcije}")
        print("=" * 40)

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    tus_zelenjava_direct()

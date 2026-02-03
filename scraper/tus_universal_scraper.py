"""
TUŠ UNIVERSAL SCRAPER - katerikoli seznam TUŠ linkov
"""

from playwright.sync_api import sync_playwright
import time
import re


def tus_universal_scraper(urls_list):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ UNIVERSAL SCRAPER ===")
        print(f"Processing {len(urls_list)} URLs...")

        total_products = 0
        total_akcije = 0
        all_results = []

        for i, url in enumerate(urls_list):
            print(f"\n--- URL {i + 1}/{len(urls_list)} ---")
            print(f"URL: {url}")

            try:
                page.goto(url)
                page.wait_for_timeout(3000)

                # POČAKAJ DA SE NALOŽI
                page.wait_for_timeout(2000)

                # SCROLL ZA VSE IZDELKE
                for j in range(5):  # 5 scrollov
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(1500)

                # POBERI VSE IZDELKE
                products = page.query_selector_all("[class*='item']")
                print(f"Najdenih {len(products)} item-ov")

                url_products = 0
                url_akcije = 0
                url_results = []

                for k, product in enumerate(products[:50]):  # prvih 50 za demo
                    try:
                        # IME - Robust selector strategy
                        name = ""
                        # Strategy 1: Specific class selectors (common in TUŠ new layout)
                        name_el = product.query_selector(".product-name, .item-name, .title")
                        if name_el:
                            name = name_el.text_content().strip()
                        
                        # Strategy 2: Heading tags fallback
                        if not name:
                            for tag in ["h3", "h4", "h5", "div[class*='name']"]:
                                name_el = product.query_selector(tag)
                                if name_el:
                                    name_text = name_el.text_content() or ""
                                    if len(name_text.strip()) > 3:
                                        name = name_text.strip()
                                        break

                        # Strategy 3: Text content heuristic (last resort)
                        if not name:
                            text = product.text_content() or ""
                            lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 3]
                            # Assume name is one of the first non-numeric lines
                            for line in lines[:3]:
                                if not any(c.isdigit() for c in line[:5]): # Heuristic: name doesn't start with numbers usually
                                    name = line
                                    break

                        # CENE - Robust extraction
                        text = product.text_content() or ""
                        # Clean price text: replace comma with dot, remove non-price chars but keep price structure
                        # Look for patterns like "1,99" or "1.99"
                        price_matches = re.findall(r'(\d+[.,]\d{2})', text)
                        
                        redna_cena = 0.0
                        akcijska_cena = 0.0
                        
                        prices = []
                        for const_p in price_matches:
                            try:
                                p_val = float(const_p.replace(",", "."))
                                prices.append(p_val)
                            except:
                                continue
                        
                        if prices:
                            prices = sorted(list(set(prices))) # Remove duplicates, sort
                            if len(prices) >= 2:
                                # Usually usually higher price is regular, lower is action
                                # But sometimes small numbers are unit prices. Heuristic: Price is usually > 0.1
                                valid_prices = [p for p in prices if p > 0.1]
                                if len(valid_prices) >= 2:
                                     redna_cena = valid_prices[-1]
                                     akcijska_cena = valid_prices[0]
                                elif len(valid_prices) == 1:
                                     redna_cena = valid_prices[0]
                            elif len(prices) == 1:
                                redna_cena = prices[0]

                        # ENOTA
                        unit = ""
                        unit_match = re.search(
                            r"(\d+\s*(?:kg|g|l|ml|kos|kom|dag))", text, re.IGNORECASE
                        )
                        if unit_match:
                            unit = unit_match.group(0)

                        # SLIKA
                        img = product.query_selector("img")
                        slika = ""
                        if img:
                            src = img.get_attribute("src") or ""
                            if src:
                                if src.startswith("data:"):
                                    pass # Skip data URIs if possible unless necessary
                                elif src.startswith("/"):
                                    slika = "https://hitrinakup.com" + src
                                else:
                                    slika = src
                            
                            # Fallback to data-src/lazyload
                            if not slika:
                                data_src = img.get_attribute("data-src")
                                if data_src:
                                    slika = data_src if data_src.startswith("http") else "https://hitrinakup.com" + data_src

                        # Shrani produkt
                        if name and redna_cena > 0:
                            url_products += 1
                            total_products += 1

                            is_akcija = (
                                akcijska_cena > 0 and akcijska_cena != redna_cena
                            )
                            if is_akcija:
                                url_akcije += 1
                                total_akcije += 1

                            product_data = {
                                "ime": name,
                                "trgovina": "Tuš",
                                "redna_cena": redna_cena,
                                "akcijska_cena": akcijska_cena if is_akcija else 0,
                                "enota": unit,
                                "slika": slika,
                                "url": url,
                                "kategorija": url.split("/")[-1]
                                if "/" in url
                                else "Unknown",
                            }

                            url_results.append(product_data)

                            # Prikaži samo prvih 10
                            if url_products <= 10:
                                status = "AKC!" if is_akcija else ""
                                print(
                                    f"  {url_products}. {name[:40]}... - {redna_cena}€ {status}"
                                )

                    except Exception as e:
                        continue

                # Shrani URL rezultate
                all_results.extend(url_results)

                print(f"URL REZULTAT: {url_products} izdelkov ({url_akcije} akcij)")

            except Exception as e:
                print(f"URL NAPAKA: {e}")

        # KONČNI REZULTATI
        print(f"\n" + "=" * 60)
        print(f"UNIVERSAL SCRAPER REZULTATI:")
        print(f"URL-ji: {len(urls_list)}")
        print(f"Skupaj izdelkov: {total_products}")
        print(f"Skupaj akcij: {total_akcije}")
        print(f"Povprečno na URL: {total_products / len(urls_list):.0f} izdelkov")
        print("=" * 60)

        return all_results


# PRIMER UPORABE:
if __name__ == "__main__":
    # DODAJ SVOJE TUŠ LINKOVE TUKAJ!
    tus_urls = [
        "https://hitrinakup.com/kategorije/Sadje%20in%20zelenjava",
        "https://hitrinakup.com/kategorije/Shramba",
        "https://hitrinakup.com/kategorije/Meso%2C%20delikatesa%20in%20ribe",
        # DODAJ ŠE VEč LINKOV ČE HOČEŠ...
    ]

    results = tus_universal_scraper(tus_urls)

    print(f"\nShranjeno {len(results)} produktov v results list!")

    input("\nPress Enter to close...")

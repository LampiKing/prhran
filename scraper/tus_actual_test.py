"""
TUŠ NOVI TEST - isci kar je na strani
"""

from playwright.sync_api import sync_playwright
import time


def tus_actual_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ DEJANSKI IZDELKI ===")

        # Odpri glavno stran
        page.goto("https://hitrinakup.com")
        page.wait_for_timeout(3000)

        # Sprejmi cookies
        try:
            page.click('button:has-text("Sprejmi")', timeout=2000)
        except:
            pass

        # Zapri popupe
        try:
            page.click('[aria-label="Close"]', timeout=2000)
            page.click('button[title="Close"]', timeout=2000)
        except:
            pass

        # Poglejmo kaj je na strani
        print("\nIskanem produkte...")

        # Išči produkte
        product_selectors = [
            "[data-testid*='product']",
            ".product-item",
            ".product-card",
            "[class*='product']",
            "article",
            ".item",
        ]

        found_products = []

        for selector in product_selectors:
            try:
                products = page.query_selector_all(selector)
                print(f"Selector {selector}: {len(products)} elementov")

                for i, product in enumerate(products[:5]):  # samo prvih 5
                    try:
                        # Ime izdelka
                        name_selectors = [
                            "h1",
                            "h2",
                            "h3",
                            "[data-testid*='name']",
                            ".product-name",
                        ]
                        name = "N/A"
                        for ns in name_selectors:
                            name_el = product.query_selector(ns)
                            if name_el:
                                name = name_el.text_content() or "N/A"
                                if name.strip():
                                    break

                        # Cena
                        price_selectors = [
                            "[data-testid*='price']",
                            ".price",
                            "[class*='cena']",
                        ]
                        price = "N/A"
                        for ps in price_selectors:
                            price_el = product.query_selector(ps)
                            if price_el:
                                price = price_el.text_content() or "N/A"
                                if price.strip():
                                    break

                        # Slika
                        img = product.query_selector("img")
                        img_src = img.get_attribute("src") if img else "N/A"

                        if name != "N/A" and len(name) > 3:
                            found_products.append(
                                {
                                    "name": name.strip(),
                                    "price": price.strip(),
                                    "image": img_src,
                                    "selector": selector,
                                }
                            )
                            print(f"  [{i + 1}] {name[:40]}... - {price}")

                    except Exception as e:
                        continue

                if found_products:
                    break

            except Exception as e:
                print(f"  Selector {selector} ni uspel: {e}")

        # Če ni našel nič, poizkusi iskanje
        if not found_products:
            print("\nPoskusim iskanje 'mleko'...")
            try:
                search_input = page.query_selector(
                    "input[type='search'], input[placeholder*='iskanje'], input[placeholder*='search']"
                )
                if search_input:
                    search_input.fill("mleko")
                    search_input.press("Enter")
                    page.wait_for_timeout(3000)

                    # Ponovno išči produkte
                    for selector in product_selectors:
                        try:
                            products = page.query_selector_all(selector)
                            print(
                                f"Iščem po iskanju - {selector}: {len(products)} elementov"
                            )
                            if products:
                                break
                        except:
                            continue
            except Exception as e:
                print(f"Iskanje ni uspelo: {e}")

        # Prikaz rezultatov
        print(f"\n" + "=" * 50)
        print(f"NAJDENI IZDELKI: {len(found_products)}")
        print("=" * 50)

        for i, product in enumerate(found_products[:2]):  # samo prva 2
            print(f"\n[IZDELEK {i + 1}]")
            print(f"Ime: {product['name']}")
            print(f"Cena: {product['price']}")
            print(
                f"Slika: {product['image'][:50]}..."
                if len(product["image"]) > 50
                else f"Slika: {product['image']}"
            )
            print(f"Selector: {product['selector']}")

        time.sleep(5)
        browser.close()


if __name__ == "__main__":
    tus_actual_test()

"""
TUŠ NEXT.JS - počakaj na dynamic content
"""

from playwright.sync_api import sync_playwright
import time


def wait_for_tus_content():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ NEXT.JS - Čakanje na content ===")

        # Capture network requests
        requests = []

        def handle_response(response):
            if "category" in response.url or "api" in response.url:
                requests.append({"url": response.url, "status": response.status})
                print(f"API Response: {response.status} - {response.url}")

        page.on("response", handle_response)

        # Odpri kategorije
        page.goto("https://hitrinakup.com/kategorije")

        print("Čakam na dynamic content...")

        # Počakaj da se React naloži
        for i in range(10):  # 10 sekund
            time.sleep(1)

            # Preveri če se je content pojavil
            try:
                # Različni možni selektorji za kategorije
                selectors = [
                    "img[src*='kategorija_']",
                    "[class*='category']",
                    "[data-testid*='category']",
                    "a[href*='/kategorije/']",
                    ".category-item",
                    "button[role='link']",
                ]

                found_any = False
                for selector in selectors:
                    elements = page.query_selector_all(selector)
                    if elements:
                        print(
                            f"Second {i + 1}: Najdenih {len(elements)} z '{selector}'"
                        )

                        # Prikaži prve elemente
                        for j, el in enumerate(elements[:3]):
                            try:
                                src = el.get_attribute("src") or ""
                                href = el.get_attribute("href") or ""
                                text = el.text_content() or ""

                                print(
                                    f"  [{j + 1}] src={src[:50]} href={href[:50]} text={text[:30]}"
                                )
                                found_any = True
                            except:
                                pass

                        if found_any and elements:
                            # Poizkusi klikniti prvo kategorijo
                            try:
                                elements[0].click()
                                page.wait_for_timeout(3000)
                                print("Kliknil prvo kategorijo!")

                                # Poglej za izdelke
                                product_selectors = [
                                    "[data-product]",
                                    ".product",
                                    "[class*='product']",
                                    "article",
                                ]

                                for ps in product_selectors:
                                    products = page.query_selector_all(ps)
                                    if products:
                                        print(f"Najdenih {len(products)} izdelkov!")

                                        # Prikaži prve 2 izdelka
                                        for k, prod in enumerate(products[:2]):
                                            try:
                                                name = ""
                                                price = ""

                                                # Iskanje imena
                                                name_el = prod.query_selector(
                                                    "h1, h2, h3, [class*='name'], [class*='title']"
                                                )
                                                if name_el:
                                                    name = name_el.text_content() or ""

                                                # Iskanje cene
                                                price_el = prod.query_selector(
                                                    "[class*='price'], [class*='cena']"
                                                )
                                                if price_el:
                                                    price = (
                                                        price_el.text_content() or ""
                                                    )

                                                img = prod.query_selector("img")
                                                img_src = (
                                                    img.get_attribute("src")
                                                    if img
                                                    else ""
                                                )

                                                print(
                                                    f"  IZDELEK {k + 1}: {name[:40]} - {price} - {img_src[:30]}"
                                                )

                                            except Exception as e:
                                                print(f"    Napaka: {e}")

                                        break

                                break
                            except Exception as e:
                                print(f"Klik ni uspel: {e}")

            except Exception as e:
                print(f"Second {i + 1}: Napaka {e}")
                continue

        print(f"\nAPI Requests: {len(requests)}")
        for req in requests:
            print(f"  {req['status']} - {req['url']}")

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    wait_for_tus_content()

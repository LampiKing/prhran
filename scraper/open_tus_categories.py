"""
TUŠ KATEGORIJE - odpri in poglej kaj je notri
"""

from playwright.sync_api import sync_playwright


def open_tus_categories():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ KATEGORIJE STRAN ===")

        # Odpri kategorije
        page.goto("https://hitrinakup.com/kategorije")

        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except:
            pass

        print("Page title:", page.title())
        print("Current URL:", page.url)

        # Sprejmi cookies
        try:
            page.click('button:has-text("Sprejmi")', timeout=3000)
            print("Clicked cookies")
        except:
            print("No cookies button")

        # Zapri popupe
        try:
            page.click('[aria-label="Close"]', timeout=2000)
            print("Closed popup")
        except:
            pass

        # Poišči kategorije
        print("\n=== ISKANJE KATEGORIJ ===")

        # Različni selektorji za kategorije
        selectors = [
            "a[href*='/kategorije/']",
            "nav a",
            ".category-item",
            ".category",
            "[data-category]",
            "li a",
            "div[class*='category'] a",
            "div[class*='Category'] a",
        ]

        found_categories = []

        for selector in selectors:
            try:
                elements = page.query_selector_all(selector)
                print(f"\nSelector {selector}: {len(elements)} elementov")

                for el in elements:
                    href = el.get_attribute("href") or ""
                    text = el.text_content() or ""

                    if text.strip() and href and "kategorije" in href:
                        if text not in [c["text"] for c in found_categories]:
                            found_categories.append(
                                {
                                    "text": text.strip(),
                                    "href": href,
                                    "selector": selector,
                                }
                            )
                            print(f"  ✓ {text.strip()} -> {href}")

                if found_categories:
                    break

            except Exception as e:
                print(f"  Selector napaka: {e}")

        # Če ni našel, poizkusi še z drugačnim pristopom
        if not found_categories:
            print("\n=== DRUGI PRISTOP ===")
            # Poglej vsak link na strani
            all_links = page.query_selector_all("a[href]")
            for link in all_links:
                href = link.get_attribute("href") or ""
                text = link.text_content() or ""

                if "hitrinakup.com/kategorije/" in href and text.strip():
                    clean_text = text.strip()
                    if clean_text and len(clean_text) > 2:
                        found_categories.append({"text": clean_text, "href": href})
                        print(f"  Link: {clean_text} -> {href}")

        # Prikaz najdenih kategorij
        print(f"\n" + "=" * 50)
        print(f"NAJDENE KATEGORIJE: {len(found_categories)}")
        print("=" * 50)

        for i, cat in enumerate(found_categories):
            print(f"[{i + 1}] {cat['text']} -> {cat['href']}")

        # Če imamo kategorije, poizkusi odprti prvo
        if found_categories:
            print(f"\nOdpiram prvo kategorijo: {found_categories[0]['text']}")
            try:
                page.goto(found_categories[0]["href"])
                page.wait_for_timeout(3000)
                print("Odprto!")

                # Poglej za izdelke
                product_selectors = [
                    "[data-product]",
                    ".product",
                    "article",
                    "[class*='item']",
                ]
                for ps in product_selectors:
                    products = page.query_selector_all(ps)
                    if products:
                        print(f"Najdenih {len(products)} produktov z: {ps}")
                        break

            except Exception as e:
                print(f"Napaka pri odpiranju: {e}")

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    open_tus_categories()

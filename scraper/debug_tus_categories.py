"""
Debug TUŠ kategorij - poglejmo kakšne kategorije so dejansko na voljo
"""

from playwright.sync_api import sync_playwright


def debug_tus_categories():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ KATEGORIJE DEBUG ===")

        # Odpri kategorije stran
        page.goto("https://hitrinakup.com/kategorije")

        # Počakaj da stran naloži
        page.wait_for_timeout(5000)

        # Sprejmi cookies če se pojavi
        try:
            page.click('button:has-text("Sprejmi")', timeout=3000)
        except:
            pass

        # Zapri popupe
        try:
            page.click('button[aria-label="Close"]', timeout=2000)
        except:
            pass

        # Poišči vse kategorije
        print("\nIskanje kategorij...")

        # Različni možni selektorji
        selectors = [
            "a[href*='/kategorije/']",
            "nav a[href*='/kategorije/']",
            ".category-item a",
            ".category a",
            "[data-testid*='category'] a",
            "li a[href*='/kategorije/']",
        ]

        for selector in selectors:
            try:
                categories = page.query_selector_all(selector)
                if categories:
                    print(f"\nNajdene kategorije z selectorjem: {selector}")
                    for i, cat in enumerate(categories):
                        text = cat.text_content() or ""
                        href = cat.get_attribute("href") or ""
                        if text and "kategorije" in href:
                            print(f"  [{i + 1}] {text.strip()} -> {href}")
            except Exception as e:
                print(f"  Selector {selector} ni uspel: {e}")

        # Poglejmo tudi HTML
        print("\nPage HTML (predelano):")
        html = page.content()
        if "kategorije/" in html:
            # Izvleci vse linije z kategorijami
            lines = html.split("\n")
            for line in lines:
                if "kategorije/" in line and "<a" in line:
                    # Enostaven extraction
                    import re

                    match = re.search(
                        r'<a[^>]+href="([^"]*kategorije/[^"]*)"[^>]*>([^<]+)</a>', line
                    )
                    if match:
                        url, name = match.groups()
                        print(f"  {name.strip()} -> {url}")

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    debug_tus_categories()

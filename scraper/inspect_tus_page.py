"""
TUŠ PAGE INSPECTION - kaj je dejansko na strani
"""

from playwright.sync_api import sync_playwright


def inspect_tus_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ PAGE INSPECTION ===")

        # Odpri glavno stran
        page.goto("https://hitrinakup.com")

        print("Page title:", page.title())
        print("Current URL:", page.url)

        # Počakaj da stran naloži
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except:
            pass

        # Sprejmi cookies
        try:
            page.click('button:has-text("Sprejmi")', timeout=3000)
            print("Clicked cookies")
        except:
            print("No cookies button found")

        # Zapri popupe
        try:
            page.click('[aria-label="Close"]', timeout=2000)
            page.click('button[title="Close"]', timeout=2000)
            print("Closed popups")
        except:
            print("No popups to close")

        # Poglej kar je na strani
        print("\n=== PAGE CONTENT ===")

        # Glavni elementi
        main_elements = ["nav", "main", "div", "section", "article", "header", "footer"]
        for tag in main_elements:
            elements = page.query_selector_all(tag)
            if elements:
                print(f"{tag}: {len(elements)} elementov")

        # Poglej vse linke
        links = page.query_selector_all("a[href]")
        print(f"\nLinkov: {len(links)}")

        # Prikaz prvih 10 linkov
        for i, link in enumerate(links[:10]):
            href = link.get_attribute("href") or ""
            text = link.text_content() or ""
            if text.strip() and href:
                print(f"  [{i + 1}] {text.strip()} -> {href}")

        # Iskanje kategorije linkov
        print(f"\n=== KATEGORIJE ===")
        category_links = []
        for link in links:
            href = link.get_attribute("href") or ""
            text = link.text_content() or ""
            if (
                "kategorije" in href
                or "Kategorije" in text
                or "category" in href.lower()
            ):
                category_links.append((text.strip(), href))
                print(f"  {text.strip()} -> {href}")

        # Poglej body content
        body_text = page.evaluate("() => document.body.innerText")
        if len(body_text) < 500:
            print(f"\nBody text: {body_text}")
        else:
            print(f"\nBody text (prvih 200): {body_text[:200]}...")

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    inspect_tus_page()

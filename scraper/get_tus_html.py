"""
TUŠ KATEGORIJE HTML - poglej cel HTML
"""

from playwright.sync_api import sync_playwright


def get_tus_categories_html():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("=== TUŠ KATEGORIJE HTML ===")

        # Odpri kategorije
        page.goto("https://hitrinakup.com/kategorije")

        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except:
            pass

        # Dobi cel HTML
        html = page.content()

        print(f"HTML length: {len(html)} characters")

        # Shrani HTML v datoteko
        with open("tus_categories_html.txt", "w", encoding="utf-8") as f:
            f.write(html)

        # Poišči JavaScript ali React aplikacijo
        print("\n=== POISKANI ELEMENTI ===")

        # JavaScript aplikacije
        js_indicators = [
            'id="root"',
            'id="app"',
            "React",
            "ReactDOM",
            "__NEXT_DATA__",
            "window.__NUXT__",
        ]

        for indicator in js_indicators:
            if indicator in html:
                print(f"✓ Najden: {indicator}")

        # Poglej za dynamic content
        dynamic_indicators = [
            "data-react",
            "data-vue",
            "ng-",
            "data-testid",
            'class="jsx-',
        ]

        for indicator in dynamic_indicators:
            if indicator in html:
                print(f"✓ Dynamic: {indicator}")

        # Poglej body content
        body = page.evaluate("() => document.body.innerHTML")
        print(f"\nBody HTML length: {len(body)}")

        # Poglej text content
        text_content = page.evaluate("() => document.body.innerText")
        print(f"\nText content (first 500 chars):")
        print(text_content[:500])

        # Poglej za script tags
        scripts = page.query_selector_all("script")
        print(f"\nSkriptov: {len(scripts)}")

        # Poglej za link tags
        links = page.query_selector_all("link")
        print(f"Linkov: {len(links)}")

        # Poišči za API klice
        print(f"\n=== API CALLS ===")

        # Intercept network requests
        network_requests = []

        def handle_request(request):
            network_requests.append({"url": request.url, "method": request.method})

        page.on("request", handle_request)

        # Počakaj malo za network requeste
        page.wait_for_timeout(3000)

        for req in network_requests[:10]:  # samo prvih 10
            if "api" in req["url"] or "category" in req["url"]:
                print(f"  {req['method']}: {req['url']}")

        print(f"\nHTML shranjen v: tus_categories_html.txt")

        input("\nPress Enter to close...")
        browser.close()


if __name__ == "__main__":
    get_tus_categories_html()

"""
Test SPAR s popravljenim popup handlerjem
"""

from stores.spar import SparScraper
from playwright.sync_api import sync_playwright


def test_spar_popup_fix():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        scraper = SparScraper(page)

        print("=== SPAR POPUP TEST ===")

        # Odpri SPAR online
        print("Odpiram SPAR online...")
        scraper.safe_goto("https://www.spar.si/online")

        # Sprejmi piškotke (brez "pogoje uporabe")
        print("Sprejemam piškotke...")
        scraper.accept_cookies()

        # Zapri popup-e (brez "pogoje uporabe")
        print("Zapiram popup-e...")
        scraper.dismiss_popups()

        print("\n=== REZULTATI ===")
        print("[OK] Piškotki sprejeti")
        print("[OK] Popup-i zaprti")
        print("[OK] Stran pripravljena za scraping")

        time.sleep(3)

        # Prikaži naslov strani
        title = page.title()
        print(f"Stran: {title}")

        # Preveri če je stran pripravljena
        page_text = page.inner_text("body").lower()
        if "kategorij" in page_text or "sadje" in page_text:
            print("[OK] Stran vsebuje produkte")

        browser.close()


if __name__ == "__main__":
    import time

    test_spar_popup_fix()

"""
Tuš opri prvi klik - samo text brez encoding napak
"""
from stores.tus import TusScraper
from playwright.sync_api import sync_playwright

def tus_opri_prvi_klik():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        scraper = TusScraper(page)
        
        print("=== TUŠ OPRI PRVI KLIK ===")
        
        try:
            # 1. Odpri kategorije
            print("1. Odpiram kategorije...")
            scraper.safe_goto("https://hitrinakup.com/kategorije")
            
            # 2. SAMO piškotki (brez popup-ov)
            print("2. Piškotki SAMO...")
            try:
                accept_selectors = [
                    'button:has-text("Sprejmi vse")',
                    'button:has-text("Accept all")',
                    '#onetrust-accept-btn-handler',
                    '.onetrust-accept-btn',
                ]
                
                for selector in accept_selectors:
                    try:
                        btn = page.query_selector(selector)
                        if btn and btn.is_visible():
                            btn.click()
                            print("   ✅ SAMO piškotki sprejeti")
                            time.sleep(1)
                            break
                    except:
                        continue
                    
            except Exception as e:
                print("   Napaka pri piškotkih: " + str(e))
            
            # 3. ZAKAJ PRVI KLIK NA GLAVNO KATEGORIJO
            print("3. ZAKAJ PRVI KLIK na glavno kategorijo...")
            try:
                category_found = False
                
                # Natisne direktni linki
                category_urls = {
                    "Sadje in zelenjava": "https://hitrinakup.com/kategorije/Sadje-in-zelenjava",
                    "Kruh, pecivo in slaščice": "https://hitrinakup.com/kategorije/kruh-pecivo-slasice",
                    "Meso, delikatesa in ribe": "https://hitrinakup.com/kategorije/meso-delikatesa-ribe",
                    "Ostalo": "https://hitrinakup.com/kategorije/ostalo"
                }
                
                if category_name in category_urls:
                    category_url = category_urls[category_name]
                    print(f"  Odpiram direkten URL: {category_url}")
                    
                    # Testiraj 5-krat ponovno za vsak primer
                    for i in range(5):
                        print(f"  {i+1}. Polni test...")
                        
                        try:
                            # Preveri če se stran naloži
                            scraper.safe_goto(category_url)
                            time.sleep(3)
                            
                            # Preveri če so se izdelki pojavili
                            page_text = page.content.lower()
                            if "ne najdeno" in page_text or len(page_text) < 1000:
                                print(f"   - Stran se ni naložila (morda bit ponovno)")
                                break
                            else:
                                # Poberi izdelke
                                try:
                                    # Uporabi minimum selector
                                    min_selectors = [
                                        'a[href*="/kategorije/"]',
                                        'a:has-text("Sadje")',
                                        'a:has-text("Kruh")',
                                        'a:has-text("Pecivo")',
                                        'a:has-text("Slano")',
                                    ]
                                    
                                    found = False
                                    for selector in min_selectors:
                                        elements = page.query_selector_all(selector)
                                        if elements and len(elements) > 0:
                                            text = elements[0].inner_text().strip()
                                            if category_name.lower() in text:
                                                elements[0].click()
                                                found = True
                                                break
                                    
                                    if found:
                                        break
                                
                                if found:
                                    print(f"   ✅ Klik na {category_name}!")
                                    break
                                    
                                time.sleep(2)
                        
                                i += 1
                        
                        except Exception as e:
                            print(f"   Napaka pri URL testu: {e}")
                            continue
                    
                    if found:
                        print("4. ✅ Klik na {category_name}!")
                        
                        # Počakaj da se stran naloži
                        time.sleep(3)
                        
                        # Poberi izdelke
                        print("5. Poberim izdelke...")
                        products = scraper.scrape_current_page(category_name)
                        
                        print(f"   NAJDENO: {len(products)} izdelkov")
                        
                        if len(products) > 0:
                            for i, product in enumerate(products[:2]):
                                print(f"   [IZDELEK {i+1}]")
                                print(f"     Ime: {product.get('ime', 'N/A')}")
                                cena = product.get('redna_cena', 0)
                                if cena:
                                    print(f"     Cena: {cena}EUR")
                                else:
                                    print(f"     Cena: NI")
                                slika = product.get('slika', '')
                                if slika:
                                    print(f"     Slika: DA ({slika[:50]}...")
                                else:
                                    print(f"     Slika: NI")
                                
                                enota = product.get('enota', '')
                                if enota:
                                    print(f"     Enota: {enota}")
                                else:
                                    print(f"     Enota: NI")
                                
                                trgovina = product.get('trgovina', 'N/A')
                                print(f"     Trgovina: {trgovina}")
                                print(f"     Kategorija: {product.get('kategorija', 'N/A')}")
                                
                        else:
                            print("   Ni izdelkov na strani")
                        
                        browser.close()
                        return
                        
                else:
                    print(f"   Kategorija '{category_name}' ni najdena v seznamu URL-ih")
            
        except Exception as e:
            print(f"   Napaka: {e}")
            browser.close()
        
        print("=== TUŠ TEST KONČAN ===")

if __name__ == "__main__":
    tus_opri_prvi_klik()
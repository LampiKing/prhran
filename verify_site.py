
import requests
import re
import sys

def check_url(url, label):
    print(f"\n--- Checking {label} ---")
    print(f"URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        html = response.text
        
        # Check Title
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        if title_match:
            print(f"Page Title: {title_match.group(1)}")
        else:
            print("Page Title: NOT FOUND")
            
        # Check for new keywords that distinguish the new version
        keywords = {
            "Začni varčevati": "New CTA detected",
            "Prihran": "Brand name detected",
            "react-native-web": "Expo Web detected",
            "entry": "Entry script detected"
        }
        
        found_any = False
        for kw, desc in keywords.items():
            if kw in html:
                print(f"✅ {desc} ('{kw}')")
                found_any = True
            else:
                print(f"❌ '{kw}' NOT FOUND")
                
        print(f"Content Length: {len(html)} bytes")
        
    except Exception as e:
        print(f"Error fetching {label}: {e}")

if __name__ == "__main__":
    # Check both the main domain and the unique deploy URL
    check_url("https://www.prhran.com", "MAIN DOMAIN")
    check_url("https://6981e355df70e7611a524956--prhrannn.netlify.app", "UNIQUE DEPLOY URL")

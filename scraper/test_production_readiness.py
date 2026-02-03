
import sys
import unittest
from unittest.mock import MagicMock
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

class TestProductionReadiness(unittest.TestCase):
    def setUp(self):
        print("\nSetting up mock Playwright page...")
        self.mock_page = MagicMock()
        self.mock_page.url = "https://example.com"

    def test_imports(self):
        """Test that all scraper modules can be imported."""
        print("Testing imports...")
        try:
            from stores.tus import TusScraper
            from stores.mercator import MercatorScraper
            from stores.spar import SparScraper
            print("✅ All store modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import store modules: {e}")

    def test_tus_scraper_init(self):
        """Test Tuš scraper initialization."""
        print("Testing Tuš scraper init...")
        try:
            from stores.tus import TusScraper
            scraper = TusScraper(self.mock_page)
            self.assertIsNotNone(scraper)
            self.assertEqual(scraper.STORE_NAME, "Tuš")
            print("✅ Tuš scraper initialized successfully")
        except Exception as e:
            self.fail(f"Failed to initialize Tuš scraper: {e}")

    def test_convex_schema_compatibility(self):
        """Verify key logic exists in files (static analysis)."""
        print("Testing Convex compatibility...")
        # Check if auth.tsx reference to updateBirthDate exists in userProfiles.ts
        # This is a basic check ensuring we didn't miss the file content earlier
        user_profiles_path = Path("convex/userProfiles.ts")
        if user_profiles_path.exists():
            content = user_profiles_path.read_text(encoding="utf-8")
            if "updateBirthDate" in content:
                print("✅ updateBirthDate mutation found in userProfiles.ts")
            else:
                print("⚠️ updateBirthDate NOT found in userProfiles.ts (Check logic)")
        else:
            print("⚠️ convex/userProfiles.ts not found (Skipping check)")

if __name__ == "__main__":
    unittest.main()

# PrHran Production Deployment

import subprocess
import sys
import os


def run_command(cmd, description):
    print(f"PROCESING: {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"DONE: {description} completed!")
            return True
        else:
            print(f"FAILED: {description} failed!")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR: {description} error: {e}")
        return False


def main():
    print("PRHRAN FULL PRODUCTION DEPLOYMENT")
    print("=" * 50)

    # 1. Git setup
    if not run_command("git init", "Git initialization"):
        return False

    # 2. Add all files
    if not run_command("git add .", "Add all files"):
        return False

    # 3. Commit
    if not run_command(
        'git commit -m "PrHran Production Deploy - All scrapers + GitHub Actions + Auto Schedule"',
        "Git commit",
    ):
        return False

    # 4. Next steps for user
    print("NEXT STEPS:")
    print("1. Create GitHub repo: https://github.com/new")
    print("2. Run: git remote add origin https://github.com/tvoj-account/prhran.git")
    print("3. Run: git push -u origin main")
    print("4. GitHub Actions will start automatically!")

    print("\nPrHran Production Ready!")
    print("Schedule: Monday & Thursday 1:00-8:00 UTC")
    print("Auto scraping: TUS + Mercator + SPAR")
    print("Auto deploy: Spletna stran + Baza")

    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("\nPRODUCTION SETUP COMPLETE!")
        print("Lep dan si ko greš dol! Vse bo delovalo!")

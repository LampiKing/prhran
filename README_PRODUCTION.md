# PrHran Production Setup

## Push na GitHub za avtomatsko delovanje:

### 1. Inštaliraj Git:
```bash
# Download: https://git-scm.com/download/win
# ali: winget install Git.Git
```

### 2. Git setup:
```bash
cd C:\Users\lampr\Desktop\PrHran
git init
git add .
git commit -m "Initial production setup"
git remote add origin https://github.com/tvoj-account/prhran.git
git push -u origin main
```

### 3. GitHub Actions za avtomatsko scraping:
- Se bo izvajalo na GitHub serverjih
- Tvoj računalnik se lahko ugasne
- Ponedeljek/Četrtek 1:00-8:00 UTC
- 100% avtomatsko

## Status:
✅ Scrapers ready (TUŠ/Mercator/SPAR)
✅ Grouping logic ready  
✅ GitHub Actions ready
✅ Auto deploy ready

## Ko se vrneš:
✅ Vse bo že delovalo avtomatsko
✅ Spletna stran posodobljena
✅ Baza podataka fresh

# PrHran je ready za production! 🚀
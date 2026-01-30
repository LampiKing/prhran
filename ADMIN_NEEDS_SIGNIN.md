# PRHRAN ADMIN - POTREBEN SIGN IN

## GitHub zahteva prijavo:

### 1. Naredi GitHub account:
- Odpri: https://github.com/signup
- Username (primer: prhran123)
- Email: tvoj.email@gmail.com
- Password: tvojeGeslo123

### 2. Potrdi email (check inbox)

### 3. Login in naredi repo:
- Sign in: https://github.com/login
- Odpri: https://github.com/new
- Repository name: `prhran`
- Public: ✅
- Create repository

### 4. Local commands (po login-u):
```powershell
cd C:\Users\lampr\Desktop\PrHran
git init
git add .
git commit -m "PrHran Production Deploy"
git remote add origin https://github.com/TVOJ_USERNAME/prhran.git
git push -u origin main
```

## ČE NE želiš registracije:
### PLAN B - Local auto-deploy:
Naredim lokalni scheduler ki bo delovalo na tvojem računalniku:
- Windows Task Scheduler
- Ponedeljek & Četrtek 1:00
- Auto scrape + deploy

## ADMIN STATUS:
✅ Vse code pripravljeno
✅ Samo potrebno GitHub account
✅ Po sign-in: 2 minute in vse deluje

# KAJ ŽELIŠ?
1. Registrirati GitHub + push?
2. Local auto-deploy (brez registracije)?

# PrHran Admin Ready! 🚀
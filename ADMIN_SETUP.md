# PRHRAN ADMIN SETUP - SAMO 3 KOMANDE!

## PRVA STVAR:
# Prenesi celega PrHran folder na GitHub
# In dodaj GitHub Actions za avtomatsko delovanje

## KORAKI:

### 1. Naredi ZIP za GitHub:
# Odprite "C:\Users\lampr\Desktop\PrHran"
# Desni klik na "PrHran" folder
# Send to → Compressed (zipped) folder
# Rezultat: "PrHran.zip"

### 2. GitHub repo:
# Odpri: https://github.com/new
# Name: prhran
# Public: YES
# Create repo

### 3. Upload ZIP:
# Na GitHub strani: "Add file → Upload files"
# Izberi "PrHran.zip"
# Upload

### 4. ZIP nastavitve:
# Ko se uploada, dodaj v root folder:
# .github/workflows/auto-scrape.yml
# vse datoteke iz PrHran folderja

## REZULTAT:
- GitHub Actions bodo zagnani
- Avtomatsko scraping bo delovalo
- Vse bo delovalo brez lokalnega računalnika

## OPTIONAL - Za hitro:
# Če imaš GitHub Desktop:
# Install GitHub Desktop
# Import PrHran folder
# Push na GitHub
# GitHub Actions bodo samodejno delovali

# Admin mode activated! 🚀
# Če hočeš, ti lahko naredim še hitrejšo verzijo.
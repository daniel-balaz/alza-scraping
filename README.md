# Alza Notebook Scraper (Playwright + Python)

Tento projekt je webový scraper pro stránku **Alza.cz**, který automaticky
načítá informace o noteboocích, prochází stránkování pomocí tlačítka
"Zobrazit více" a ukládá data do souboru `notebooks.csv`.

Scraper je napsaný v **Pythonu** pomocí **Playwrightu** a pracuje
s reálným prohlížečem (Chromium).

---

## Funkce

- Vyhledá a načte požadovaný počet produktů.
- Extrahuje tyto informace:
  - Název notebooku
  - Cena
  - Hodnocení a počet hodnocení
  - Dostupnost
  - URL obrázku
  - URL produktu
  - ID produktu
  - Parametry: RAM, SSD kapacitu, CPU model
- Vyhne se duplikovaným URL.
- Ukládá výsledek jako **CSV** (`notebooks.csv`).
- Ochranné mechanismy (nepůsobí jako bot):
  - User-Agent
  - Odstranění `navigator.webdriver`
  - Náhodné prodlevy

---

## Technologie

- **Python 3.10+**
- **Playwright (sync API)**
- **Pandas**
- **Chromium browser**

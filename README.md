# Olympic Games Data Analysis - Kanada

Komplett lösning för Projekt_OS - Olympic Games Data Analysis med fokus på Kanada.

## Dataset

- **Källa**: [120 years of Olympic history: athletes and results](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)
- **Fil**: `data/athlete_events.csv`
- **Storlek**: ~200MB, 271,116 rader, 15 kolumner
- **Licens**: CC0: Public Domain

## Installation

1. Klona repositoryt eller ladda ner filerna
2. Installera dependencies:

```bash
pip install -r requirements.txt
```

3. Ladda ner datasetet från Kaggle och placera det i `data/athlete_events.csv`

## Användning

### Task 0: Exploratory Data Analysis (EDA)

Öppna Jupyter Notebook:

```bash
jupyter notebook notebooks/01_exploratory_analysis.ipynb
```

Notebooket innehåller:
- Grundläggande statistik (antal länder, sporter, medaljtyper)
- Åldersstatistik
- Visualiseringar (könsfördelning, toppländer, medaljer över tid, åldersfördelning)
- Kanada-specifik analys

### Task 1 & 2: Modulär Python-kod

#### Data Loader (`src/data_loader.py`)

Laddar och anonymiserar data med SHA256-hash:

```python
from src.data_loader import load_and_anonymize_data

df = load_and_anonymize_data('data/athlete_events.csv')
```

#### Data Processor (`src/data_processor.py`)

OOP-baserad analysklass:

```python
from src.data_processor import OlympicAnalyzer

analyzer = OlympicAnalyzer(df)
top_sports = analyzer.top_sports_by_medals('CAN')
medals_per_year = analyzer.medals_per_olympics('CAN')
```

### Task 3: Plotly Dash Dashboard

Kör dashboarden:

```bash
python -m src.dashboard
```

Eller:

```bash
cd src
python dashboard.py
```

Dashboarden öppnas på `http://localhost:8050` och innehåller:

- **Landstatistik (Kanada som standard)**:
  - Top sporter med flest medaljer
  - Medaljer per OS
  - Åldersfördelning
  - Fördelning av medaljtyper

- **Sportstatistik**:
  - Medaljer per land för vald sport
  - Åldersfördelning
  - Könsfördelning
  - Medaljtyper

## Funktioner

### GDPR-kompatibel anonymisering

- Idrottarnas namn hashas med SHA256
- Originalnamn tas bort från datasetet
- Hashade namn används för analys

### Modulär kodstruktur

- OOP-baserad design med `OlympicAnalyzer`-klass
- Separata moduler för datahantering och visualisering
- Återanvändbar kod

### Interaktiv dashboard

- Plotly Dash för interaktiva visualiseringar
- Callback-funktioner för realtidsuppdateringar
- Enhetlig design med CSS-styling

## Källhänvisningar

**VIKTIGT**: Alla källor och referenser finns dokumenterade i `CITATIONS.md`.

Huvudsakliga källor:
- **Dataset**: Kaggle - 120 years of Olympic history
- **Libraries**: Pandas, Plotly Dash, NumPy, Matplotlib, Seaborn
- **Documentation**: Se `CITATIONS.md` för fullständig lista

All kod i detta projekt är original implementation, men använder dokumentation och best practices från ovanstående källor.

## Deployment

### Render/Heroku

1. Skapa `Procfile` (redan inkluderad):
```
web: gunicorn src.dashboard:app.server
```

2. Deploy till Render eller Heroku

### Lokal körning

```bash
python -m src.dashboard
```
## Tekniska detaljer

### Designprinciper

- **Enhetlig färgpalett**: Viridis och Plasma palettes för färgblind-vänlighet
- **Responsiv layout**: Anpassar sig till olika skärmstorlekar
- **Progressiv disclosure**: Användaren väljer land/sport stegvis

### Visualiseringar

- **Horisontella stapeldiagram**: Lättare att läsa långa sportnamn
- **Färggradienter**: Snabbt visar intensitet utan att överbelasta
- **Linjediagram över tid**: Tydlig trendvisualisering för tidsbaserade data

## Författare

Projekt_OS - Olympic Games Data Analysis

## Licens

Detta projekt är skapat för utbildningssyfte.

## Källhänvisningar

Se `CITATIONS.md` för fullständig lista över alla källor, bibliotek och referenser som används i detta projekt.

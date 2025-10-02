# UFC Analysis (Streamlit)

Live-scraped UFC fight analytics focused on **winner vs loser** stats.
The app pulls completed events directly from **UFC Stats** and presents
simple, readable charts suitable for a portfolio/demo.

## What’s in here
- `scrapers/` — pure scraping functions that **return DataFrames** (no CSV writing).
- `streamlit/app.py` — the Streamlit UI (caching, progress bar, filters).
- `ufc_data/` — optional cached CSVs copied from the legacy repo (the app does **not** use them).

## Why this repo
The original code wrote CSVs and relied on them for notebooks. This refactor
keeps the scrapers reusable and lets the Streamlit app fetch **fresh data in-memory**
without touching your notebook CSVs.

## Run it
```bash
# 1) Create a virtual env (recommended)
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Launch the app
streamlit run streamlit/app.py
```

## In the app
- **Fetch scope** (sidebar): choose **Latest N** events (fast) or **Since date**.
- Progress bar while scraping; results are **cached** for the same parameters.
- Filters for **date range** and **weight class**.
- Charts: Winner vs Loser means, Outcome distribution, Submission distribution.
- Men’s weight-class ordering used for nicer menus.

## Notes & sources
- Events and results are scraped from the UFC Stats *Completed Events* page. See the official listing for current events and historical archive. 
- The scraper structure here was inspired by community datasets (e.g., Kaggle projects that source from UFC Stats).
- Please be considerate to the UFC Stats website. Add delays or reduce fetch scope if you hit blocks.

**Official sources**
- UFC Stats — Completed Events: https://ufcstats.com/statistics/events/completed
- UFC Weight Classes overview: https://www.ufc.com/news/understanding-ufc-weight-classes-and-weigh-ins

## Requirements
See `requirements.txt` for exact versions. Core libs:
- requests, beautifulsoup4
- pandas, numpy
- matplotlib
- streamlit
- tqdm (optional; not used in the UI path)
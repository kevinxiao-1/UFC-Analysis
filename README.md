# UFC Data Analysis

This repository explores modern UFC fight data to understand which in-cage stats correlate with winning. It includes lightweight scrapers to refresh the dataset and a polished analysis notebook that produces hiring-portfolio-ready visuals.

## Repository Layout
- `scrapers/`: Stand-alone scripts (sourced from [Fatbardh Smajli's Kaggle project](https://www.kaggle.com/datasets/fatismajli/ufc-data)) for collecting fight- and fighter-level data from ufcstats.com.
- `ufc_data/`: Cached CSV exports created by the scrapers (`ufc_event_data.csv`, `ufc_fighters.csv`).
- `analysis_portfolio_v2.ipynb`: Portfolio-ready notebook that cleans the raw tables, engineers winner/loser features, and visualizes key trends.
- `analysis_portfolio_v1.ipynb`: Earlier draft kept for reference.

## Getting Started
1. **Install Python 3.9+** and create a virtual environment if desired.
2. **Install dependencies:**
   ```bash
   pip install pandas matplotlib seaborn requests beautifulsoup4 tqdm jupyter
   ```
3. (Optional) Launch Jupyter Lab/Notebook to browse the analyses:
   ```bash
   jupyter lab
   ```

## Refreshing the Data
> The bundled CSVs cover events through 30 Aug (most recent update when the notebook was last run). Re-run the scrapers whenever you need fresh data.

The scrapers write directly into `ufc_data/` and will overwrite existing files. Running both scripts is enough to fully refresh the dataset.

```bash
python3 scrapers/events_scraper.py    # fight-level stats per event
python3 scrapers/fighter_data_scraper.py  # roster snapshot with physical attributes
```

Each script iterates over every UFC event/fighter page, so expect a few minutes of network traffic. Be considerate when scraping; throttle manually if you encounter rate limits.

## Notebook Workflow
The main analysis lives in `analysis_portfolio_v2.ipynb`. It is structured for readability with short sections and explicit takeaways.

High-level flow:
1. **Load & preview** `ufc_event_data.csv` and `ufc_fighters.csv`.
2. **Clean & standardize** columns (dates, winner/loser stat splits, missing values) while keeping the code resilient to column-name drift.
3. **Explore** descriptive statistics and correlations for winner vs. loser striking/grappling metrics.
4. **Visualize outcomes** such as finish method distributions and submission breakdowns (with grouped "Other" category for readability).

Key insights surfaced by the current dataset:
- Winners typically lead clearly in significant strikes, takedowns landed, submission attempts, and knockdowns.
- Decisions remain the dominant fight outcome, with KO/TKOs and submissions forming most of the remaining finishes.
- Rear naked chokes and guillotine variants top the submission leaderboard, while rarer subs are rolled into an "Other" bucket to keep charts legible.

Run the notebook top-to-bottom after refreshing the data to reproduce the figures. The code depends only on the CSVs shipped in `ufc_data/`.

## Extending the Project
- Add feature engineering (e.g., per-minute rates, fighter reach/height merges) to deepen the winner vs. loser analysis.
- Introduce automated tests or data validation to flag unexpected schema changes from the UFC Stats site.
- Export visuals to image files or dashboards for easier sharing.

## Attribution
The scraping logic is adapted (with credit noted in-source) from Fatbardh Smajli's Kaggle dataset. All analysis code and commentary in this repository build on those raw exports.

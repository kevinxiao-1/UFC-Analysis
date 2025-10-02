import sys
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Ensure project root (parent of this file's directory) is on sys.path
ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scrapers.events import scrape_all_events

st.set_page_config(page_title="UFC Analysis", page_icon="🥊", layout="wide")

@st.cache_data(show_spinner=True)
def load_data():
    return scrape_all_events()

def main():
    st.title("📊 UFC Analysis - Winner vs Loser")
    st.markdown("""
    **Goal:** Identify which fight stats correlate with winning.
    **Scope:** Modern UFC fights scraped from ufcstats.com.
    """)

    # Load data
    df = load_data()
    st.write("### Raw Data", df.head())

    # Example chart: Fight outcomes
    if "Method" in df.columns:
        method_counts = df["Method"].value_counts()
        fig, ax = plt.subplots()
        method_counts.plot(kind="bar", ax=ax)
        ax.set_title("Fight Outcomes (Grouped)")
        st.pyplot(fig)

if __name__ == "__main__":
    main()

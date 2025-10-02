from __future__ import annotations

from datetime import datetime
from typing import Callable, Iterable, Optional

import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Be polite: set a common User-Agent
UA = {"User-Agent": "Mozilla/5.0"}

COMPLETED_URL = "http://ufcstats.com/statistics/events/completed?page=all"

def _clean_cell(text: str) -> str:
    return re.sub(r"\s+", "-", text.strip().replace("\n", ""))

def get_event_index(session: Optional[requests.Session] = None) -> list[dict]:
    """
    Return a newest-first list of dicts: {url, name, date(datetime)}
    pointing to individual event result pages on ufcstats.com.
    """
    s = session or requests.Session()
    resp = s.get(COMPLETED_URL, headers=UA, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")
    rows = soup.select("tr.b-statistics__table-row")[2:]  # skip header rows

    out: list[dict] = []
    for r in rows:
        a = r.select_one("a")
        if not a or not a.get("href"):
            continue
        name = a.text.strip()
        href = a["href"]
        tds = r.select("td")
        date_txt = tds[-1].text.strip() if tds else ""
        try:
            dt = datetime.strptime(date_txt, "%B %d, %Y")
        except Exception:
            # If parsing fails, leave as None; we'll still scrape by URL order
            dt = None
        out.append({"url": href, "name": name, "date": dt})
    return out  # newest-first

def scrape_fight_data(event_url: str, session: Optional[requests.Session] = None) -> list[list]:
    """
    Scrape a single event page for fight rows.
    Returns a list of rows with fixed schema (see columns below).
    """
    s = session or requests.Session()
    resp = s.get(event_url, headers=UA, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "html.parser")
    fights: list[list] = []

    title = soup.find("h2", class_="b-content__title")
    event_name = title.text.strip() if title else "Unknown Event"

    li = soup.find("li", class_="b-list__box-list-item")
    event_date = li.text.strip().split("\n")[-1].strip() if li else ""

    table = soup.find("table", class_="b-fight-details__table")
    if not table:
        return fights

    rows = table.find_all("tr", class_="b-fight-details__table-row")[1:]  # skip header
    for row in rows:
        cols = row.find_all("td", recursive=False)
        if len(cols) < 10:
            continue

        flag = cols[0].find("i", class_="b-flag__inner")
        result = " ".join(flag.text.split()) if flag else ""
        fighters = [a.text.strip() for a in cols[1].find_all("a")]
        if len(fighters) != 2:
            # sometimes missing, skip row
            continue
        fighter1, fighter2 = fighters

        kd = _clean_cell(cols[2].text)
        strikes = _clean_cell(cols[3].text)
        td = _clean_cell(cols[4].text)
        sub = _clean_cell(cols[5].text)
        weight_class = cols[6].text.strip()
        method = _clean_cell(cols[7].text)
        round_ = cols[8].text.strip()
        time_ = cols[9].text.strip()

        if result == "win":
            winner = fighter1
        elif result == "draw":
            winner = "Draw"
        else:
            winner = "NC"

        fights.append([
            event_name, event_date, winner, fighter1, fighter2,
            kd, strikes, td, sub, weight_class, method, round_, time_
        ])
    return fights

def scrape_all_events(*,
                      limit: Optional[int] = None,
                      since: Optional[datetime] = None,
                      stop_at_seen: Optional[set[tuple[str, datetime]]] = None,
                      progress: Optional[Callable[[int, int], None]] = None,
                      session: Optional[requests.Session] = None) -> pd.DataFrame:
    """
    Scrape multiple events efficiently.

    Parameters
    ----------
    limit : int, optional
        Only fetch the newest N events.
    since : datetime, optional
        Only fetch events whose date >= since (requires date to parse).
    stop_at_seen : set[(name, date)], optional
        If provided, stop once we encounter a seen (name, date).
    progress : callable(i, total), optional
        Called after each event is scraped (for Streamlit progress bars).
    session : requests.Session, optional
        Use a provided session (helps with connection reuse).

    Returns
    -------
    pd.DataFrame with columns:
        ["Event Name","Event Date","Result","Fighter1","Fighter2",
         "KD","Strikes","TD","Sub","Weight Class","Method","Round","Time"]
    """
    s = session or requests.Session()
    idx = get_event_index(session=s)  # newest-first

    # Filter by since
    if since is not None:
        idx = [it for it in idx if (it["date"] is not None and it["date"] >= since)]

    # Trim by stop_at_seen sequentially
    if stop_at_seen:
        trimmed = []
        for it in idx:
            if it["date"] is not None:
                key = (it["name"], it["date"].date())
                if key in stop_at_seen:
                    break
            trimmed.append(it)
        idx = trimmed

    # Limit final list
    if limit is not None:
        idx = idx[:max(0, int(limit))]

    rows, total = [], len(idx)
    for i, it in enumerate(idx, 1):
        rows.extend(scrape_fight_data(it["url"], session=s))
        if progress:
            progress(i, total)

    cols = ["Event Name","Event Date","Result","Fighter1","Fighter2",
            "KD","Strikes","TD","Sub","Weight Class","Method","Round","Time"]
    return pd.DataFrame(rows, columns=cols)
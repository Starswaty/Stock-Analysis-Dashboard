import requests
import pandas as pd
import time
import os
from datetime import datetime
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Updated headers to closely mimic a real browser request
NSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.nseindia.com/"
}

BASE_URL = "https://www.nseindia.com/api/quote-equity"

# Custom cookies from the previous input
CUSTOM_COOKIES = {
    "_abck": "B0C130E6630ADCE054CADAD039F8FB11~0~YAAQIiEPFxeLFIyWAQAArf9IoQ0OEnnAKKcqytcmJOfkiVbFOw0ixhMCIE1DO1x6o4htreGK4m6/yV8op6A9dnBZRE7xsNuTj16/kmkYvz0WfbGLKhdo9urUshBC21pOsEqiHrZBRTmfoTD/c6DQ1Jm1nY2uIhFxYJUJbGBsnPCHakaZWCcxoVRy2N0XM/xGhchmLAGFX0Mty47LLdP84azTCsvbgphttNgewtWqSUjhw+lG1shxh9zMtxU8t1KDCGfRQLXHQ7ip/tAsNnT9ngGSlc6XEbhY/EUsogv8GXfLvzE/oh5bi8XR99ieU/zl4oinbeaBx+D9ZKp0GtT274LjXYtv5rstvNa8rnwyvaAPMPudGoJOlyg8gS5f/8VHprmJLy0BZ+Wwuk3+QBRZFZ7lBqaRqTBedXHCf6q6vp69HCMOJtICJoWGyTTuh5aBQYQv4bgKmF7w1WZudFdiHNo/0h0zls8SFxWKQ/03rzBxeSPKt2wRWdEtmkSVcsWBSTAVsXzp7W7Z3BPUtxmqPjIUkyWoq6FM+h1baTAQKD3M7wcVuB5TyEuGWDGJvIhSy5FEORpyvIH5SriRKO11YZSehJ+d~-1~||0||~-1",
    "ak_bmsc": "1B487312B84F4C667C5C17E6E95462E0~000000000000000000000000000000~YAAQIiEPF92SFIyWAQAAS89JoRvrbb+RAYyJE2LuYIzJimpTJD1QvjWojqjsYduJ60FzJd3T48oLL5F+Qzz+HQeLrpaNXHMSq9O4jkv4fW9uEK4me13mX+TTiJ+7HTpRsshO7etpQN9FfSDexKQTYql4OPV71AJLAgenrOdA5pDsNOZQPN6JSgAaJcAI5Fg/Ish9SPzohvCObMpjtd3M8N31RQdgEEpf9MIjG5pxltoMqzyN3HZP94vA0ycxarkbpmt4KHUqrkq/IjR+l6ji4jzldYMGznNAyarGbI4dTno6/Mdz9PIBt5BfgkYS1LVecG6++dXF5pLMF3oI7GiIjs8ieQJiWufxy5s0txb8afzkkUqtCeeZJF5RM5dMoj3djkfqiWj3oo2FjDG6Z5+hGUyn3MxsSVnz6B+UOJ87OO6VJq71MvXJV62j7BqgurlcGBVrnAIIIwRvsxkbNL6vVuUcsiAx5ZKNrXnpN89jNdAih61cJbuYnua9T66S42b696R23UrOTVOR0jEbi8jvddFC1yIfrLnVkU9frMvUNX8=",
    "bm_sv": "919FFA61BD89AC2DEA296252C802FEF5~YAAQIiEPF1+RFIyWAQAAc59JoRsbZMsR52xlsLv7WD9z9JrAtdMxvCu24Cqo8oMS0nHlzCguSpCbGH2/fkHHbekLAunJb1MFRgp7EduQMcER0XWy02c5zBtNJBsEkGKA0a/TMFvhJqvLiDHK7UfBhostSGtODeIM0WtVqKaFB2ZpSF99XvVjoIW5YppqzvcaVOeHIgc3jq1VKW+Qwx4uRq8VduvXshfeoa9uktf9KAnQfGFMIEbfg1crITUks4Ojfozy~1",
    "nseappid": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTc0NjQ2MjYzMywiZXhwIjoxNzQ2NDY5ODMzfQ._NupsDinFhRDC7mW6cFOLR0TUGaLt8f2RXGinDlLYEw",
    "nsit": "kVRT8A2unr3KtcD1_gf1FNuU"
}

# Global session
session = requests.Session()
session.headers.update(NSE_HEADERS)
session.cookies.update(CUSTOM_COOKIES)

def setup_nse_session():
    try:
        print("[~] Initializing session with NSE homepage...")
        response = session.get("https://www.nseindia.com", timeout=10)
        cookies = session.cookies.get_dict()
        print(f"[✓] Session initialized successfully. Cookies: {cookies}")
        time.sleep(5)
    except Exception as e:
        print(f"[!] Failed to initialize session: {e}")

def get_realtime_data(symbol):
    url = f"{BASE_URL}?symbol={symbol.upper()}"
    try:
        response = session.get(url, timeout=10)

        if response.status_code == 401:
            print(f"[!] {symbol} - Unauthorized. Check your session or headers.")
            return None
        elif response.status_code == 429:
            print(f"[!] Rate limit hit for {symbol}. Sleeping for 60 seconds...")
            time.sleep(60)
            return get_realtime_data(symbol)
        
        if response.status_code != 200:
            print(f"[!] {symbol} - Unexpected response status: {response.status_code}")
            return None

        data = response.json()
        quote = data.get("priceInfo", {})
        meta = data.get("metadata", {})

        return {
            "symbol": symbol.upper(),
            "companyName": meta.get("companyName"),
            "lastPrice": quote.get("lastPrice"),
            "change": quote.get("change"),
            "pChange": quote.get("pChange"),
            "dayHigh": quote.get("intraDayHighLow", {}).get("max"),
            "dayLow": quote.get("intraDayHighLow", {}).get("min"),
            "totalTradedVolume": quote.get("totalTradedVolume"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"[!] Error fetching {symbol}: {e}")
        return None

def poll_realtime_quotes(symbols, interval_seconds=10, duration_minutes=1, output_csv=None):
    """
    Polls real-time data for a list of symbols every 'interval_seconds' for 'duration_minutes'.
    Appends data to CSV after each poll.
    """
    if output_csv is None:
        output_csv = os.path.join(DATA_DIR, "realtime_feed.csv")
    else:
        if not os.path.isabs(output_csv):
            output_csv = os.path.join(DATA_DIR, output_csv)

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    total_polls = int((duration_minutes * 60) / interval_seconds)
    print(f"[✓] Starting real-time polling for {symbols} every {interval_seconds}s for {duration_minutes} minutes...")

    for i in range(total_polls):
        batch = []
        print(f"[~] Poll {i+1}/{total_polls} at {datetime.now().strftime('%H:%M:%S')}")

        for symbol in symbols:
            quote = get_realtime_data(symbol)
            if quote:
                print(f"  → {symbol}: ₹{quote['lastPrice']} ({quote['pChange']}%)")
                batch.append(quote)

        if batch:
            df = pd.DataFrame(batch)
            write_header = not os.path.exists(output_csv) or os.stat(output_csv).st_size == 0
            df.to_csv(output_csv, mode='a', index=False, header=write_header)

        time.sleep(interval_seconds)

    print(f"[✓] Polling finished. Output saved to {output_csv}")

if __name__ == "__main__":
    setup_nse_session()

    # User input: comma-separated symbols
    user_input = input("Enter comma-separated NSE symbols (e.g., TCS, INFY, RELIANCE): ")
    symbols = [s.strip().upper() for s in user_input.split(",") if s.strip()]

    poll_realtime_quotes(
        symbols=symbols,
        interval_seconds=10,
        duration_minutes=1
        # No need to pass output_csv; will default to data/realtime_feed.csv
    )


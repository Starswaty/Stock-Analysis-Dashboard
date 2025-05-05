# ingestion/fx.py

import requests
import pandas as pd
import os
from datetime import datetime

def fetch_live_fx_rates():
    base_currencies = ['usd', 'eur', 'jpy', 'chf']
    results = {}
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for base in base_currencies:
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            inr_value = data.get(base, {}).get('inr')
            results[f"{base.upper()}/INR"] = inr_value
        except Exception as e:
            results[f"{base.upper()}/INR"] = None
            print(f"[✗] Error fetching {base.upper()}/INR: {e}")

    # Convert to DataFrame
    df = pd.DataFrame([results])
    df.insert(0, 'Timestamp', timestamp)

    # Save to CSV
    os.makedirs("data", exist_ok=True)
    output_path = "data/fx_rates.csv"
    df.to_csv(output_path, index=False)

    print("[✓] FX Rates Fetched and Saved to data/fx_rates.csv")
    return df

if __name__ == "__main__":
    fetch_live_fx_rates()

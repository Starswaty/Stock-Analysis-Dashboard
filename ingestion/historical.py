import requests
import pandas as pd
import os
from datetime import datetime

def fetch_historical_data(symbol: str, start_date: str = None) -> pd.DataFrame:
    """
    Fetch historical stock data for a given symbol from the custom NSE API,
    save it as a CSV in the data folder, and return it as a DataFrame.

    Args:
        symbol (str): Ticker symbol (e.g., "INFY", "TCS").
        start_date (str): Optional. Filter data from this date (YYYY-MM-DD).

    Returns:
        pd.DataFrame: Historical stock data.
    """
    api_url = "https://nse-data-api.onrender.com/historical/"
    params = {"symbol": symbol}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        data = response.json().get("data", [])
        df = pd.DataFrame(data)

        if not df.empty and 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

            if start_date:
                start = pd.to_datetime(start_date)
                df = df[df['date'] >= start]

            df = df.sort_values("date").reset_index(drop=True)

            # Ensure data directory exists
            os.makedirs("data", exist_ok=True)
            file_path = os.path.join("data", f"{symbol}_historical_data.csv")
            df.to_csv(file_path, index=False)

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

import pandas as pd
from zoneinfo import ZoneInfo
from datetime import datetime
import os

def save_csv(data, log_dir):
    file_timestamp = datetime.now(ZoneInfo("America/Toronto")).strftime("%Y-%m-%d_%H-%M-%S")
    csv_file = f'{log_dir}/log_{file_timestamp}.csv'
    df = pd.DataFrame(data, columns=["Timestamp", "Shortened Timestamp", "Temperature", "Humidity"])
    df.to_csv(csv_file, index=False)
    print(f"Data saved to {csv_file}")

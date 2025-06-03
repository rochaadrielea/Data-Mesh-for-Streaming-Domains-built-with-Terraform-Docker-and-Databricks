import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from devops.terraform.utils.blob_uploader import upload_to_blob

def generate_weather(n_records=1440):
    now = datetime.now()
    timestamps = [now - timedelta(minutes=i) for i in range(n_records)]

    data = {
        "timestamp": [ts.isoformat() for ts in timestamps],
        "temperature_C": np.random.normal(loc=20, scale=5, size=n_records).round(1),
        "humidity_%": np.random.normal(loc=60, scale=10, size=n_records).round(1),
        "wind_speed_kmh": np.random.normal(loc=15, scale=3, size=n_records).round(1),
        "precip_mm": np.random.exponential(scale=1.0, size=n_records).round(2)
    }

    return pd.DataFrame(data)

if __name__ == "__main__":
    # 1. Generate the data
    df = generate_weather()

    # 2. Prepare the output path
    now = datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    output_dir = os.path.join("data_simulator", "landing", date_str, "weather")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"weather_{now.strftime('%H-%M-%S')}.json"
    full_path = os.path.join(output_dir, filename)

    # 3. Save to file
    df.to_json(full_path, orient="records", lines=False)
    print(f"✅ Weather file saved: {full_path}")

    # 4. Upload to Azure Blob
    upload_to_blob(full_path, layer="bronze", domain="weather")

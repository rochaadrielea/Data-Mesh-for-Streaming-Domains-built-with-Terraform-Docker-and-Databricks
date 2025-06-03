import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from devops.terraform.utils.blob_uploader import upload_to_blob

def generate_energy_costs(n_records=168):  # hourly for 7 days
    now = datetime.now()
    timestamps = [now - timedelta(hours=i) for i in range(n_records)]

    data = {
        "timestamp": [ts.isoformat() for ts in timestamps],
        "provider": [random.choice(["ABB Energy", "GridCo", "PowerX"]) for _ in range(n_records)],
        "cost_per_kwh": np.random.uniform(0.08, 0.18, n_records).round(3)
    }

    return pd.DataFrame(data)


if __name__ == "__main__":
    # 1. Generate Data
    df = generate_energy_costs()

    # 2. Prepare local path
    now = datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    output_dir = os.path.join("data_simulator", "landing", date_str, "energy_costs")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"energy_costs_{now.strftime('%H-%M-%S')}.json"
    full_path = os.path.join(output_dir, filename)

    # 3. Save to local file
    df.to_json(full_path, orient="records", lines=False)
    print(f"✅ Saved file: {full_path}")

    # 4. Upload to Azure Blob
    upload_to_blob(full_path, layer="bronze", domain="energy_costs")
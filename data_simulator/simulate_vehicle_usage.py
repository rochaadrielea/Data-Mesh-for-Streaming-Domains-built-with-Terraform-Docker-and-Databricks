import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from devops.terraform.utils.blob_uploader import upload_to_blob

def generate_vehicle_usage(n_units=10, n_records=300):
    unit_ids = [f'TU_{i}' for i in range(1, n_units + 1)]
    now = datetime.now()

    usage = []
    for _ in range(n_records):
        unit = random.choice(unit_ids)
        timestamp = now - timedelta(hours=random.randint(0, 72))
        usage_hours = round(np.random.uniform(1, 12), 2)
        route = random.choice(["R1", "R2", "R3", "R4"])
        status = random.choice(["Active", "Idle", "Maintenance", "Standby"])
        usage.append({
            "unit_id": unit,
            "timestamp": timestamp.isoformat(),
            "route": route,
            "usage_hours": usage_hours,
            "status": status
        })

    return pd.DataFrame(usage)

if __name__ == "__main__":
    # 1. Generate the data
    df = generate_vehicle_usage()

    # 2. Prepare the output path
    now = datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    output_dir = os.path.join("data_simulator", "landing", date_str, "vehicle_usage")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"vehicle_usage_{now.strftime('%H-%M-%S')}.json"
    full_path = os.path.join(output_dir, filename)

    # 3. Save to file
    df.to_json(full_path, orient="records", lines=False)
    print(f"✅ File created: {full_path}")

    # 4. Upload to Azure Blob
    upload_to_blob(full_path, layer="bronze", domain="vehicle_usage")

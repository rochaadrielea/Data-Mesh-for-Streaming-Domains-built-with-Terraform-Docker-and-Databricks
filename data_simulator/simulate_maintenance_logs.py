import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from devops.terraform.utils.blob_uploader import upload_to_blob

def generate_maintenance_logs(n_units=10, n_logs=100):
    unit_ids = [f'TU_{i}' for i in range(1, n_units + 1)]
    now = datetime.now()

    logs = []
    for _ in range(n_logs):
        unit = random.choice(unit_ids)
        timestamp = now - timedelta(hours=random.randint(1, 48))
        fault_code = random.choice([0, 1, 2])
        description = random.choice([
            "Brake calibration", "Oil change", "Power anomaly", "Sensor check", "Routine inspection"
        ])
        technician = random.choice(["Alex", "Samira", "Lee", "Fernando", "Anja"])
        logs.append({
            "unit_id": unit,
            "timestamp": timestamp.isoformat(),
            "fault_code": fault_code,
            "description": description,
            "technician": technician
        })

    return pd.DataFrame(logs)

if __name__ == "__main__":
    # 1. Generate the Data
    df = generate_maintenance_logs()

    # 2. Build Output Path
    now = datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    output_dir = os.path.join("data_simulator", "landing", date_str, "maintenance")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"maintenance_logs_{now.strftime('%H-%M-%S')}.json"
    full_path = os.path.join(output_dir, filename)

    # 3. Save to Local File
    df.to_json(full_path, orient="records", lines=False)
    print(f"✅ Saved: {full_path}")

    # 4. Upload to Azure Blob
    upload_to_blob(full_path, layer="bronze", domain="maintenance")

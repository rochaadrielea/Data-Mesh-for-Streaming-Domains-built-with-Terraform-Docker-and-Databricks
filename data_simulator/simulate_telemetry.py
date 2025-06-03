import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from devops.terraform.utils.blob_uploader import upload_to_blob

def generate_telemetry(n_units=10, n_records_per_unit=1440):
    start_time = datetime.now() - timedelta(days=1)

    def simulate_unit_data(unit_id):
        timestamps = [start_time + timedelta(minutes=i) for i in range(n_records_per_unit)]
        temperature = np.random.normal(loc=75, scale=5, size=n_records_per_unit)
        vibration = np.random.normal(loc=50, scale=10, size=n_records_per_unit)
        power_draw = np.random.normal(loc=120, scale=15, size=n_records_per_unit)

        fault_code = []
        for t, v in zip(temperature, vibration):
            if t > 90 or v > 80:
                fault_code.append(2)
            elif t > 85 or v > 70:
                fault_code.append(1)
            else:
                fault_code.append(0)

        print(f"✅ Simulation complete for unit {unit_id}")
        return pd.DataFrame({
            'unit_id': unit_id,
            'timestamp': timestamps,
            'temperature': temperature.round(2),
            'vibration': vibration.round(2),
            'power_draw': power_draw.round(2),
            'fault_code': fault_code
        })

    all_data = pd.concat([simulate_unit_data(f'TU_{i}') for i in range(1, n_units+1)], ignore_index=True)
    return all_data

if __name__ == "__main__":
    # 1. Generate Data
    df = generate_telemetry()

    # 2. Prepare output path
    now = datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    output_dir = os.path.join("data_simulator", "landing", date_str, "telemetry")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"telemetry_{now.strftime('%H-%M-%S')}.json"
    full_path = os.path.join(output_dir, filename)

    # 3. Save to file
    df.to_json(full_path, orient="records", lines=False)
    print(f"✅ Saved telemetry file: {full_path}")

    # 4. Upload to Azure Blob (bronze layer)
    upload_to_blob(full_path, layer="bronze", domain="telemetry")

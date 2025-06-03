import argparse

from data_simulator.simulate_telemetry import generate_telemetry
from data_simulator.simulate_maintenance_logs import generate_maintenance_logs
from data_simulator.simulate_vehicle_usage import generate_vehicle_usage
from data_simulator.simulate_weather import generate_weather
from data_simulator.simulate_energy_costs import generate_energy_costs
from devops.terraform.utils.blob_uploader import upload_to_blob
from devops.terraform.utils.blob_initializer import initialize_blob_folders
import os
from datetime import datetime

# Map domain to function
jobs = {
    "telemetry": generate_telemetry,
    "maintenance": generate_maintenance_logs,
    "vehicle_usage": generate_vehicle_usage,
    "weather": generate_weather,
    "energy_costs": generate_energy_costs
}

def save_and_upload(domain, df, run_time, base_folder):
    domain_folder = os.path.join(base_folder, domain)
    os.makedirs(domain_folder, exist_ok=True)
    filename = f"{domain}_{run_time}.json"
    path = os.path.join(domain_folder, filename)
    df.to_json(path, orient="records", lines=True)
    print(f"✅ Saved to local: {path}")
    upload_to_blob(path, layer="bronze", domain=domain)
    print(f"☁️ Uploaded {domain} data to blob.")

def run_simulation(domain):
    now = datetime.now()
    date_folder = f"{now.year}/{now.month:02d}/{now.day:02d}"
    run_time = now.strftime("%H-%M-%S")
    base_folder = os.path.join("data_simulator", "landing", date_folder)

    os.makedirs(base_folder, exist_ok=True)
    initialize_blob_folders()

    if domain == "all":
        for name, generator in jobs.items():
            print(f"\n🚀 Generating data for: {name}")
            df = generator()
            save_and_upload(name, df, run_time, base_folder)
    elif domain in jobs:
        print(f"\n🚀 Generating data for: {domain}")
        for i in range(5):
         df = jobs[domain]()
         timestamped_run = f"{run_time}_{i}"
         save_and_upload(domain, df, timestamped_run, base_folder)
    else:
        print(f"❌ Unknown domain: {domain}. Choose from: {list(jobs.keys()) + ['all']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate and upload domain data.")
    parser.add_argument("--domain", required=True, help="Domain to simulate (e.g. telemetry, maintenance, all)")
    args = parser.parse_args()
    run_simulation(args.domain)
#     print(f"❌ Unknown domain: {args.domain}. Choose from: {list(jobs.keys()) + ['all']}")
#     run_simulation(args.domain)
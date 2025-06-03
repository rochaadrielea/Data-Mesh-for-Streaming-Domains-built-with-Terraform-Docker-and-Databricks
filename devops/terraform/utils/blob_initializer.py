import os
import json
from azure.storage.blob import BlobServiceClient

# Fix: get absolute path to secrets.json based on script location
base_dir = os.path.dirname(os.path.abspath(__file__))
secrets_path = os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'secrets', 'secrets.json'))

with open(secrets_path) as f:
    secrets = json.load(f)

AZURE_CONN_STR = secrets["AZURE_CONN_STR"]
CONTAINER = "telemetry-data"  # <- Replace with your actual container if different

# Define all layers and domains
LAYERS = ["bronze", "silver", "gold"]
DOMAINS = ["telemetry", "maintenance", "weather", "vehicle_usage", "energy_costs"]

def initialize_blob_folders():
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONN_STR)

    for layer in LAYERS:
        for domain in DOMAINS:
            blob_path = f"{layer}/{domain}/_init.txt"
            blob_client = blob_service_client.get_blob_client(container=CONTAINER, blob=blob_path)

            if not blob_client.exists():
                blob_client.upload_blob(b"initialized", overwrite=False)
                print(f"✅ Created folder: {layer}/{domain}/")
            else:
                print(f"✔️ Folder already exists: {layer}/{domain}/")

if __name__ == "__main__":
    initialize_blob_folders()
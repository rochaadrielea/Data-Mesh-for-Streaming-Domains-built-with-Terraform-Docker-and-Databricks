import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime
import json

# Fix: get absolute path to secrets.json based on script location
base_dir = os.path.dirname(os.path.abspath(__file__))
secrets_path = os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'secrets', 'secrets.json'))

with open(secrets_path) as f:
    secrets = json.load(f)

AZURE_CONN_STR = secrets["AZURE_CONN_STR"]
CONTAINER = "telemetry-data"

def upload_to_blob(local_path, layer="bronze", domain="telemetry"):
    date_parts = local_path.split(os.sep)[-4:-1]  # [YYYY, MM, DD]
    print(f"date_parts: {date_parts}")
    filename = os.path.basename(local_path)
    print(f"filename: {filename}")
    blob_path = f"{layer}/{domain}/{'/'.join(date_parts)}/{filename}"
    print(f"Blob path: {blob_path}")

    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
    blob_client = blob_service_client.get_blob_client(container=CONTAINER, blob=blob_path)
    print(f"Blob client: {blob_client}")

    if blob_client.exists():
        print(f"⚠️ File already exists in Azure Blob: {blob_path}")
    else:
        with open(local_path, "rb") as data:
            blob_client.upload_blob(data)
        print(f"✅ Uploaded to blob: {blob_path}")

        
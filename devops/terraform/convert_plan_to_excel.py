import os
import json
import csv
import subprocess

# Generate fresh plan.json from tfplan.binary
print("🛠️ Regenerating plan.json...")
subprocess.run("terraform show -json tfplan.binary > plan.json", shell=True)

# Check file exists and is not empty
if not os.path.exists("plan.json") or os.path.getsize("plan.json") == 0:
    print("❌ plan.json is missing or empty. Did terraform show fail?")
    exit(1)

# Load and convert
with open("plan.json") as f:
    plan = json.load(f)

changes = plan.get("resource_changes", [])

with open("plan_export.csv", "w", newline="") as csvfile:
    fieldnames = ["action", "resource_type", "resource_name", "address", "replace_reason"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for change in changes:
        for action in change["change"]["actions"]:
            writer.writerow({
                "action": action,
                "resource_type": change.get("type"),
                "resource_name": change.get("name"),
                "address": change.get("address"),
                "replace_reason": change.get("action_reason", "")
            })

print("✅ Done! Exported to plan_export.csv")
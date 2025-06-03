# 🛠️ How to Use the RailSightX++ Platform (Updated)

This guide is tailored for team members working on the **evolving version** of the RailSightX++ project. It covers hierarchical usage depending on project roles and progress.

---

## 🧱 1. Infrastructure Provisioning (Terraform)

> If not yet applied on Azure, provision the storage layer using Terraform:

```bash
cd devops/terraform
terraform init
terraform apply
```

**Creates:**
- Azure Resource Group
- Azure Storage Account
- Azure Blob Container (`telemetry-data`)

---

## 🧪 2. Environment Setup (First-Time and Repeat)

### Create & Activate Virtual Environment

```bash
python3 -m venv railsight_env
source railsight_env/bin/activate  # or .\railsight_env\Scripts\activate on Windows
```

### Install All Required Dependencies

```bash
pip install -r requirements.txt
```

📄 [requirements.txt](../requirements.txt)

---

## 🐳 3. Docker Image (Rebuild if Code Changes)

```bash
docker build -t railsimulator:latest .
docker tag railsimulator:latest railsightregistry.azurecr.io/railsimulator:latest
docker push railsightregistry.azurecr.io/railsimulator:latest
```

---

## ☸️ 4. Run Kubernetes CronJobs

> Simulators run every 5 minutes and use blob utilities to push JSON to Bronze Layer.

```bash
kubectl apply -f devops/k8s/
```

📁 [CronJobs YAML](../devops/k8s/)

---

## ⚙️ 5. Blob Folder Initialization (if not done yet)

```bash
python utils/blob_initializer.py
```

📄 [blob_initializer.py](../utils/blob_initializer.py)

---

## 📤 6. Optional Manual Upload / Watcher

Upload test data manually:

```bash
python utils/blob_uploader.py
```

Or use the folder watcher:

```bash
python utils/folder_watcher.py
```

📂 [utils/](../utils/)

---

## 💾 7. Databricks Full Pipeline Execution

Open and run the notebook/script:

```python
notebooks/databricks_ingestion/full_pipeline_with_ml.py
```

Includes:
- Bronze ➝ Silver ➝ Gold
- ML pipeline + MLflow logging
- SHAP explainability

📄 [full_pipeline_with_ml.py](../notebooks/databricks_ingestion/full_pipeline_with_ml.py)

---

## 📊 8. Connect to Power BI or Dashboards

Power BI can be connected to Gold tables via:
- Azure Synapse (SQL)
- Databricks SQL endpoint
- Or CSV download from Databricks workspace

---

## 🚧 Developer Workflow Tips

| Task                             | Action                                      |
|----------------------------------|---------------------------------------------|
| Added simulator?                | Add YAML + update Docker image              |
| Changed utils?                  | Rebuild Docker + test with watcher          |
| Changing pipeline logic?        | Update `full_pipeline_with_ml.py`           |
| Adding model registry?          | Use `ml/registry/`                          |
| Updating SHAP visualizations?   | Edit `ml/explainability/`                   |
| Adding a new dashboard?         | Place it under `dashboards/`                |

---

## 📁 Project Hierarchy Overview

```
RAILSIGHTX++
├── data_simulator/
├── devops/
│   ├── terraform/ (IaC for Azure)
│   └── k8s/       (CronJobs for simulation)
├── ml/
│   ├── experiments/
│   ├── explainability/
│   └── registry/
├── notebooks/
│   └── databricks_ingestion/
├── utils/         (uploader, folder watcher)
├── dashboards/
├── secrets/       (.env and keys – never push!)
├── requirements.txt
├── Dockerfile
├── Docker-compose.yaml
```

---

> This flow ensures both new contributors and active developers can execute, test, and evolve the system in a structured way. Terraform lays the foundation; Docker and k8s simulate; Databricks transforms; ML adds value.

# A Scalable Azure-First Streaming Data Lakehouse Pipeline with ML, Kubernetes, and Terraform



---

## 🔍 Overview

RailOpsStreamX simulates a complete **streaming Data Lakehouse architecture** for railway operations using:

- **Python** for data simulation
- **Azure Blob Storage** for scalable data ingestion
- **Azure Databricks + PySpark** for streaming transformations
- **Delta Lake** with Bronze, Silver, Gold structure
- **Random Forest ML model** for predictive maintenance
- **Power BI** for real-time reporting dashboards
- **Kubernetes (k8s)** to orchestrate simulation jobs
- **Terraform** to provision Azure resources (Storage, Databricks, etc.)

---

## ⚙️ Pipeline Structure

```
[Data Simulators] --> [Local Bronze Folders] --> [Azure Blob Storage: /bronze/<domain>]
                                                   ⬇
                                    [Databricks Autoloader + PySpark]
                                                   ⬇
                       /silver/<domain>    -->    Cleaned & normalized
                       /gold/<domain>      -->    Aggregated & scored by ML model
```

---

## 🧱 Data Domains

Simulated every 5 minutes using Kubernetes CronJobs:

- `telemetry`: sensor logs (speed, vibration, fault flags)
- `vehicle_usage`: trip durations, loads, engine time
- `maintenance`: scheduled tasks, costs, delays
- `energy_costs`: fuel or electricity metrics
- `weather`: synthetic regional conditions

---

## 🧠 Machine Learning Model (Databricks)

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
```

Stored model is logged with MLFlow for versioning and performance tracking.

---

## 🌐 Terraform Integration

Infrastructure-as-code provisioning includes:

- Azure Storage Account
- Azure Databricks Workspace + Cluster
- Key Vault (for secrets)
- Resource Group & Role assignments

```hcl
resource "azurerm_storage_account" "railops" {
  name                     = "storagerailnortheurope"
  resource_group_name      = azurerm_resource_group.railops.name
  location                 = "North Europe"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```

---

## ☸️ Kubernetes Integration

Each data simulator is containerized and triggered via **Kubernetes CronJob**:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: telemetry-simulator
spec:
  schedule: "*/5 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: telemetry-sim
              image: railops/telemetry-sim:latest
          restartPolicy: OnFailure
```

---

## 📊 Power BI Dashboard

- Connected directly to `gold` layer via Azure Blob or Synapse
- Real-time indicators include:
  - Fault prediction heatmaps
  - Energy efficiency over time
  - Maintenance delay risk zones

---

## 🔄 Agile Workflow

- Each stage is tracked using GitHub Projects (Kanban-style)
- Issues are tagged: `terraform`, `databricks`, `ml`, `infra`, `dashboards`
- Example tasks: `#21: Add bronze retention policy`, `#42: Tune RandomForest params`

---

## 🎓 Exam Alignment: AZ-104

- ✅ Azure Storage, IAM & keys ✅ Blob Containers & access control
- ✅ Databricks workspace & cluster creation via portal/CLI
- ✅ Resource Group setup & permissions
- ✅ Infrastructure lifecycle automation using Terraform

---

## ✅ Use Cases

- Real-time railway data simulation
- Predictive maintenance systems
- Scalable ingestion & ML pipelines on Azure
- Interview-ready data engineering demo

---

## 📁 Project Tree

```
.
├── data_simulator/
│   ├── simulate_telemetry.py
│   ├── simulate_maintenance.py
├── devops/
│   ├── telemetry-cronjob.yaml
├── terraform/
│   ├── main.tf
├── notebooks/
│   ├── Bronze_Ingestion.ipynb
│   ├── ML_Model_Scoring.ipynb
├── dashboards/
│   ├── PowerBI_RailOps.pbix
├── README.md
```

---

## 📌 Status

- ✅ Blob ingestion + Autoloader
- ✅ ML scoring + model logging
- ✅ Kubernetes orchestration (telemetry + vehicle_usage)
- ✅ Terraform infrastructure provisioning( azure and k8s provisioned via devops/terraform/main.tf)
- 🔲 Synapse integration (up next)
- 🔲 CI/CD pipeline via GitHub Actions

---

## 💬 Contributing

PRs welcome for:
- ML model improvement
- Dashboard templates (Power BI / Streamlit)
- Infra upgrade suggestions

---

## License

MIT © 2025 RailOpsStreamX Contributors

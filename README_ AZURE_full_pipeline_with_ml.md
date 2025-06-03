# Databricks Full Pipeline (Bronze → Silver → Gold → ML)

This repository showcases a complete end-to-end data engineering and machine learning pipeline built on Azure Databricks using PySpark. It is designed to ingest, clean, enrich, and train predictive models using real-time telemetry and operational data.

---

## 🧱 Architecture Overview

```
Terraform → Azure Blob (Bronze) → Databricks (Silver, Gold) → ML Model → MLflow → Dashboard/Inference
```

---

## 🎯 Use Case

This project simulates a **predictive maintenance** system for a rail or industrial fleet, where:
- Data from sensors and maintenance logs is streamed into a Bronze layer.
- Data is cleaned in Silver.
- Transformed into features in Gold.
- A machine learning model is trained and logged with MLflow.

---

## 🧪 Technology Stack

| Layer        | Tools                                      |
|--------------|--------------------------------------------|
| Infrastructure | Terraform, Azure Resource Group/Blob Storage |
| Ingestion    | Databricks, PySpark, ABFSS                 |
| Processing   | Delta Lake (Bronze → Silver → Gold)        |
| ML & Logging | PySpark MLlib, MLflow                      |
| Secrets Mgmt | `.env`, `os.getenv()`                      |

---

## 🔐 Secure Configuration

All secrets and sensitive values are stored as environment variables:

```bash
AZURE_STORAGE_ACCOUNT=your-storage-account-name
AZURE_CONTAINER_NAME=telemetry-data
AZURE_ACCESS_KEY=your-secret-access-key
```

Use the provided `.env.example` as a safe template.

---

## 🚦 Pipeline Stages

### 1. Bronze Layer – Real-Time Ingestion
- Streaming JSON files from simulated watchdog data
- Stored in Delta tables as raw historical data

### 2. Silver Layer – Cleaning
- Drops fully-null rows
- Standardizes format for downstream processing

### 3. Gold Layer – Enrichment
- Adds `date`, `time` columns
- Replaces all nulls with "unknown"
- Reorders columns for analytics/ML readiness

### 4. Machine Learning – Model Training
- Filters telemetry_gold where `fault_code` exists
- Trains RandomForestClassifier on `engine_temp`, `speed`, `load`
- Logs accuracy and model with MLflow for versioning

---

## 📁 Folder Structure

```
notebooks/
└── databricks_pipeline/
    └── full_pipeline_with_ml.py
.env.example
README.md
```

---

## 📊 Sample Output

```
✅ Loaded 1050 rows into: telemetry_bronze
✅ Processed Silver table: telemetry_silver
✅ Saved Gold table: telemetry_gold
🎯 Accuracy: 0.88
✅ Model logged with MLflow
```

---

## 📌 MLflow Integration

The experiment is tracked in:
```
/Users/adriel.mlflow/telemetry_rf
```

It includes:
- Parameters (`features`, `label`)
- Accuracy metric
- Serialized Spark ML model

---

## 🤖 Extend This Project

- Add SHAP for model interpretability
- Visualize fault detection results in Power BI
- Set up model scoring with Databricks Jobs or Airflow

---

## 👩‍💻 Author

**Adriel Rocha**  
Azure Data Engineer | ML-Driven Architecture | Zurich 🇨🇭

---


---

## 🔍 Model Interpretability with SHAP (Coming Soon)

To increase trust and transparency in the machine learning model, we plan to integrate **SHAP (SHapley Additive exPlanations)**:

- Visualize which features influence predictions most
- Explain anomalies and fault predictions
- Help domain experts understand model behavior

Example extension (coming soon):

```python
import shap

# Convert Spark DataFrame to Pandas
pandas_df = test_df.select("features").toPandas()

# Initialize SHAP explainer
explainer = shap.Explainer(model.featureImportances.toArray(), pandas_df)
shap_values = explainer(pandas_df)

# Plot
shap.summary_plot(shap_values, pandas_df)
```

This will be part of our next iteration of `full_pipeline_with_ml.py`.

---

"""
full_pipeline_with_ml.py

Complete PySpark pipeline from Bronze to Silver to Gold layer,
including machine learning model training, evaluation, and logging with MLflow.

Secrets are managed securely using environment variables.

Author: Adriel
"""

import os
from pyspark.sql.functions import col, lit, coalesce, date_format
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import mlflow
import mlflow.spark

# ✅ Step 1: Define secure variables
storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT")  # e.g. "storagepredictivedata"
container_name = os.getenv("AZURE_CONTAINER_NAME", "telemetry-data")
access_key = os.getenv("AZURE_ACCESS_KEY")

# ✅ Step 2: Set Spark config for ABFSS (Azure Blob Filesystem - Secure)
spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
    access_key
)

# ✅ Step 3: Define domains
domains = ["telemetry", "weather", "vehicle_usage", "maintenance", "energy_costs"]

# ✅ Step 4: Bronze Ingestion - Streaming JSON to Bronze Tables
for domain in domains:
    path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/bronze/{domain}/landing/2025/06/02/{domain}/"
    try:
        df = (
            spark.read
            .format("json")
            .option("recursiveFileLookup", "true")
            .option("multiline", "true")
            .load(path)
        )
        print(f"✅ Loaded {df.count()} rows into: {domain}_bronze")
        df.write.mode("overwrite").saveAsTable(f"{domain}_bronze")
    except Exception as e:
        print(f"❌ Failed to load {domain}: {e}")

# ✅ Step 5: Silver Transformation - Drop nulls
for domain in domains:
    try:
        bronze_df = spark.read.table(f"{domain}_bronze")
        silver_df = bronze_df.dropna(how="all")
        silver_df.write.mode("overwrite").saveAsTable(f"{domain}_silver")
        print(f"✅ Processed Silver table: {domain}_silver")
    except Exception as e:
        print(f"❌ Error in Silver layer for {domain}: {e}")

# ✅ Step 6: Gold Transformation - Enrich and clean for ML
for domain in domains:
    try:
        silver_df = spark.read.table(f"{domain}_silver")
        if "timestamp" in silver_df.columns:
            silver_df = (
                silver_df
                .withColumn("date", date_format("timestamp", "dd/MM/yyyy"))
                .withColumn("time", date_format("timestamp", "HH:mm:ss"))
                .drop("timestamp")
            )
        for col_name in silver_df.columns:
            silver_df = silver_df.withColumn(
                col_name, coalesce(col(col_name).cast("string"), lit("unknown"))
            )
        cols = silver_df.columns
        if "date" in cols and "time" in cols:
            cols.remove("date")
            cols.remove("time")
            silver_df = silver_df.select(["date", "time"] + cols)
        silver_df.write.mode("overwrite").saveAsTable(f"{domain}_gold")
        print(f"✅ Saved Gold table: {domain}_gold")
    except Exception as e:
        print(f"❌ Error in Gold layer for {domain}: {e}")

# ✅ Step 7: ML Pipeline - Train RandomForestClassifier (example: telemetry)
try:
    df = spark.read.table("telemetry_gold")
    df = df.filter(col("fault_code").isNotNull())

    # Select features and label
    features = ["engine_temp", "speed", "load"]
    label = "fault_code"

    df = df.select(*features, label).dropna()

    # Assemble features
    assembler = VectorAssembler(inputCols=features, outputCol="features")
    df = assembler.transform(df).select("features", label)

    # Train/test split
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    # Train model
    rf = RandomForestClassifier(featuresCol="features", labelCol=label, numTrees=10)
    model = rf.fit(train_df)

    # Predict
    predictions = model.transform(test_df)

    # Evaluate
    evaluator = MulticlassClassificationEvaluator(labelCol=label, predictionCol="prediction", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions)
    print(f"🎯 Accuracy: {accuracy:.2f}")

    # ✅ Log model with MLflow
    mlflow.set_experiment("/Users/adriel.mlflow/telemetry_rf")
    with mlflow.start_run():
        mlflow.log_param("features", features)
        mlflow.log_param("label", label)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.spark.log_model(model, "telemetry_rf_model")
        print("✅ Model logged with MLflow")

except Exception as e:
    print(f"❌ ML pipeline failed: {e}")


# ✅ Step 8: SHAP Explainability (Optional but Recommended)
try:
    import shap
    import pandas as pd

    # Convert a sample of test data to Pandas
    pandas_df = test_df.select("features").toPandas()

    # Extract raw feature importances from the trained model
    feature_importances = model.featureImportances.toArray()

    # Create SHAP explainer using feature importances as a proxy
    explainer = shap.Explainer(lambda x: feature_importances, pandas_df)
    shap_values = explainer(pandas_df)

    # Plot summary
    shap.summary_plot(shap_values, pandas_df)

    print("✅ SHAP summary plot generated.")

except Exception as e:
    print(f"❌ SHAP failed: {e}")

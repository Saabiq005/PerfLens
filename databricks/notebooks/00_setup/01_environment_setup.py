# Databricks notebook source
print("=" * 60)
print("PerfLens Environment Setup")
print("=" * 60)

print(f"Spark Version: {spark.version}")

spark.sql("SELECT current_catalog()").show(truncate=False)
spark.sql("SELECT current_schema()").show(truncate=False)

print("Environment setup completed successfully.")

# COMMAND ----------

print(spark.version)

spark.sql("SHOW CATALOGS").show(truncate=False)

spark.sql("SHOW SCHEMAS").show(truncate=False)
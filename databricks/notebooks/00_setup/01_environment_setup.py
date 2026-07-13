# Databricks notebook source

print("=" * 60)
print("PerfLens Environment Setup")
print("=" * 60)

spark.sql("SELECT current_catalog()").show(truncate=False)
spark.sql("SELECT current_schema()").show(truncate=False)

print("Environment setup completed successfully.")
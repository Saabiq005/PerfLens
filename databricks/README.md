# PerfLens Databricks Platform

## Purpose

This directory contains the Databricks implementation of the PerfLens analytics platform.

## Architecture

Kafka
    ↓
Bronze
    ↓
Silver
    ↓
Gold
    ↓
AI
    ↓
Power BI

## Responsibilities

Bronze
- Raw telemetry ingestion
- Immutable storage

Silver
- Parsing
- Normalization
- Data quality

Gold
- KPIs
- Analytics
- AI-ready datasets

AI
- Feature engineering
- Summarization
- Recommendations

Reporting
- Power BI datasets
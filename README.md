# PerfLens

> AI-Powered Application Performance Data Pipeline

![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

# Overview

PerfLens is an end-to-end AI-powered Application Performance Data Pipeline designed to provide intelligent performance observability across distributed applications.

Traditional monitoring platforms expose metrics, logs and traces but still require engineers to manually correlate telemetry across multiple systems before identifying the root cause of performance degradation.

PerfLens extends conventional observability by combining telemetry collection, data engineering, artificial intelligence and business intelligence into a single automated pipeline capable of:

- Collecting application telemetry
- Building a historical analytics dataset
- Detecting anomalies
- Generating AI-assisted root cause analysis
- Producing executive performance reports
- Visualizing trends through interactive dashboards

The project is inspired by enterprise observability platforms while remaining completely buildable using open-source software and free cloud tiers.

---

# Problem Statement

Modern applications produce enormous amounts of telemetry.

However, organizations commonly face several challenges:

- Fragmented telemetry across multiple tools
- No centralized historical performance dataset
- Manual investigation of incidents
- Reactive performance monitoring
- Limited visibility into deployment impact
- Difficulty measuring optimization improvements

PerfLens addresses these problems through an AI-assisted data pipeline capable of transforming raw telemetry into actionable insights.

---

# Objectives

The primary objectives of PerfLens are:

- Standardize application telemetry
- Collect metrics, traces and events
- Build a Bronze → Silver → Gold analytics pipeline
- Detect anomalies using AI
- Generate root cause hypotheses
- Produce weekly AI-generated reports
- Visualize application health through dashboards
- Demonstrate an enterprise-grade Data Engineering workflow

---

# High Level Architecture

```
┌────────────────────┐
│ Application A      │
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│ OpenTelemetry SDK  │
└─────────┬──────────┘
          │
      OTel Collector
          │
     ┌────┴─────┐
     │          │
     ▼          ▼
Azure Monitor  Redis Pub/Sub
                  │
                  ▼
         Python Consumer
                  │
                  ▼
        Databricks Delta Lake
         Bronze → Silver → Gold
                  │
      ┌───────────┴────────────┐
      ▼                        ▼
 Gemini AI              Claude AI
      │                        │
      └────────────┬───────────┘
                   ▼
            Power BI Dashboard
```

---

# Core Features

## Application Instrumentation

- OpenTelemetry SDK
- Distributed Tracing
- Metrics Collection
- Error Monitoring
- Latency Monitoring

---

## Streaming Layer

- Redis Pub/Sub
- Real-time Telemetry
- Event-driven Architecture

---

## Data Engineering

- Bronze Layer
- Silver Layer
- Gold Layer
- Delta Lake
- Historical Analytics

---

## Artificial Intelligence

Gemini is responsible for:

- Anomaly Detection
- Root Cause Suggestions
- Severity Classification
- Performance Narratives

Claude is responsible for:

- Weekly Executive Reports
- AI-assisted Documentation
- Performance Summaries

---

## Dashboards

Power BI dashboards provide:

- Latency Trends
- Error Rate Trends
- Throughput Analysis
- Trace Analytics
- AI Annotation Feed

---

# Technology Stack

| Layer | Technology |
|---------|------------|
| Language | Python 3.11 |
| Instrumentation | OpenTelemetry |
| Message Broker | Redis Pub/Sub |
| Monitoring | Azure Monitor |
| Data Engineering | Databricks |
| Storage | Delta Lake |
| AI | Gemini 2.5 Flash |
| AI Reporting | Claude Sonnet |
| Dashboard | Power BI |
| Testing | Pytest |
| Data Validation | Great Expectations |
| Load Testing | Locust |
| CI/CD | GitHub Actions |
| Version Control | Git |

---

# Repository Structure

```
PerfLens/

├── configs/
├── data/
├── docker/
├── docs/
├── notebooks/
├── scripts/
├── src/
├── tests/
├── README.md
└── requirements.txt
```

---

# Development Roadmap

The project is divided into multiple independent milestones.

| Milestone | Description |
|------------|-------------|
| 1 | Project Foundation |
| 2 | Development Environment |
| 3 | Telemetry Simulator |
| 4 | OpenTelemetry Integration |
| 5 | Redis Streaming |
| 6 | Bronze Pipeline |
| 7 | Silver Pipeline |
| 8 | Gold Pipeline |
| 9 | Gemini AI |
| 10 | Claude Reports |
| 11 | Power BI |
| 12 | QA Framework |
| 13 | End-to-End Integration |
| 14 | Documentation & Release |

---

# Testing Strategy

PerfLens follows a shift-left testing philosophy.

Testing includes:

- Unit Testing
- Integration Testing
- End-to-End Testing
- Data Quality Validation
- AI Evaluation
- Load Testing
- Continuous Integration

---

# Project Status

Current Phase:

**Milestone 1 — Project Foundation**

Upcoming:

- Repository Setup
- Environment Configuration
- Architecture Documentation

---

# Future Enhancements

Potential future improvements include:

- Kubernetes Deployment
- Kafka Streaming
- ML-based Forecasting
- Multi-cloud Monitoring
- Grafana Dashboards
- OpenSearch Integration
- Real-time Alerting
- Slack & Microsoft Teams Notifications



# Author

**Saabiq Ahamed**

AI • Data Engineering • Cloud • DevOps • Observability
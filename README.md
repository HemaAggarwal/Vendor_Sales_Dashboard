# Vendor Sales Performance Dashboard

## 📊 Project Overview
This project delivers a comprehensive, end-to-end data analytics solution designed to evaluate and optimize supply-chain performance, pricing strategies, and profitability across multiple vendor networks. Processing over *550+ transactions* stretching across 10 global vendors, 5 distinct regions, and 8 product categories, the pipeline transforms raw operational tracking logs into strategic business insights[cite: 1]. The architecture manages an asset ecosystem generating over *₹12 crore in total revenue*[cite: 1].

The pipeline follows the industry-standard *CRISP-DM* (Cross-Industry Standard Process for Data Mining) methodology, moving seamlessly from data ingestion and cleaning to structured transformations and executive visualization.

---

## 🛠️ Architecture & Tech Stack
The project is built on a modular four-tier stack to demonstrate competency across core modern data tools:

*   *Data Cleaning & Processing (Python):* Scripted imputation models utilizing pandas and numpy to handle structural anomalies, clean null fields, and engineer chronological features.
*   *Relational Storage & Modeling (SQL):* Structured queries executing precise multi-dimensional aggregations, sales breakdowns, and cross-tabulations.
*   *Ad-hoc Analysis (Excel):* Dynamic pivot architectures, interactive slicers, and conditional logic matrices for localized, rapid exploration.
*   *Business Intelligence & Reporting (Power BI):* Interactive executive reporting layer driven by optimized *DAX (Data Analysis Expressions)* measures.

---

## 📁 Repository Structure
```text
├── data/
│   └── vendor_sales_data.csv          # Raw and cleaned transaction dataset[cite: 1]
├── notebooks_scripts/
│   └── vendor_python_analysis.py      # Python script for data processing & imputation[cite: 1]
├── sql/
│   └── queries.sql                    # SQL scripts for metrics extraction and aggregation
├── bi_dashboards/
│   ├── vendor_sales_dashboard.xlsx    # Excel Pivot table analysis framework[cite: 1]
│   └── vendor_sales_dashboard.pbix    # Power BI dashboard workbook file
├── documentation/
│   └── project_documentation.html     # Deep-dive technical project documentation[cite: 1]
└── README.md                          # Repository documentation

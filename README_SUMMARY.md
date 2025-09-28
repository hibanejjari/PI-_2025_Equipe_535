# PI-_2025_Equipe_535

## Overview
This project, carried out **with Vinci Energies**, sets up a **data analytics pipeline** for data quality and dashboard supervision.

It integrates:
- **dbt** → transforms raw data into clean, reliable tables  
- **PostgreSQL** → stores both raw and transformed datasets  
- **Python** → automation, anomaly detection, and validation  
- **Apache Superset** → dashboards & KPIs (read-only, for business users)  
- **Generative AI (future extension)** → natural-language anomaly explanations, summaries, and auto-reports  

### Workflow
```text
┌───────────────┐     ┌───────────────┐
│   Raw Data    │ ──► │      dbt      │
└───────────────┘     └───────┬───────┘
                              │
                              ▼
                     ┌───────────────┐
                     │  PostgreSQL   │
                     │ - Stores raw  │
                     │   & clean     │
                     └───────┬───────┘
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
        ┌───────────────┐       ┌───────────────┐
        │    Python     │       │   Superset    │
        │ - Automation  │       │ - Dashboards  │
        │ - Anomaly ML  │       │ - Charts/KPIs │
        │ - Validation  │       │   (read-only) │
        └───────┬───────┘       └───────────────┘
                │
                ▼
        ┌───────────────┐
        │ Generative AI │
        │ - Explanations│
        │ - Summaries   │
        │ - Auto-Reports│
        └───────────────┘
```

---

## Table of Contents
1. [Overview](#overview)  
2. [Quickstart](#quickstart)  
   - [Start Superset (Docker)](#1-start-superset-docker)  
   - [Install dbt (PostgreSQL)](#2-install-dbt-postgresql)  
   - [Configure PostgreSQL Connection](#3-configure-postgresql-connection)  
   - [Test + Run First Model](#4-test--run-first-model)  
   - [Visualize in Superset](#5-visualize-in-superset)  
3. [Key Files](#key-files)  
4. [References](#references)  
5. [Working with Git](GIT_WORKFLOW.md)  
6. [Generative AI Extension](#generative-ai-extension)  

---

## Quickstart

### 1. Start Superset (Docker)
```bash
git clone https://github.com/apache/superset.git
cd superset
docker compose -f docker-compose-non-dev.yml up -d
```
Access at: [http://localhost:8088](http://localhost:8088)  
Login: `admin / admin`

---

### 2. Install dbt (PostgreSQL)
```bash
cd ~/Documents
python -m venv dbt_env
source dbt_env/bin/activate   # (Linux/Mac)
dbt init my_project
```
On Windows:
```powershell
C:\Users\<YourName>\Documents\dbt_env\Scripts\activate
```
Install dbt:
```bash
pip install dbt-postgres
```

---

### 3. Configure PostgreSQL Connection
Create file: `~/.dbt/profiles.yml`  
```yaml
my_project:
  outputs:
    dev:
      type: postgres
      host: localhost
      user: postgres
      password: your_password_here
      port: 5432
      dbname: postgres
      schema: public
  target: dev
```

---

### 4. Test + Run First Model
```bash
cd ~/Documents/my_project
dbt debug      # test connection
```

Inside `models/hello_world.sql`:
```sql
SELECT 1 AS id, 'hello_dbt' AS message
```

Run:
```bash
dbt run
```

Check in PostgreSQL:
```sql
SELECT * FROM hello_world;
```
Expected output:  
`1 | hello_dbt`

---

### 5. Visualize in Superset
- Go to **Superset → Data → Datasets → + Dataset**  
- Select your PostgreSQL DB  
- Create a chart → add it to a dashboard  

---

## Key Files
- `models/*.sql` → dbt transformations  
- `~/.dbt/profiles.yml` → PostgreSQL connection config  
- `scripts/superset_check.py` → validate dashboards vs reference data  
- `.gitlab-ci.yml` → CI/CD pipeline setup  

---

## Generative AI Extension
The pipeline can be extended with **Generative AI** to improve explainability:  
- Provide natural-language explanations for anomalies detected by Python.  
- Summarize dashboards into plain-text insights for business users.  
- Generate automated reports directly from PostgreSQL + Superset results.  

**Tools to consider:**  
- OpenAI API (GPT models) for reports.  
- Hugging Face Transformers for summarization.  
- LangChain for combining SQL queries and LLMs.  

---

## References
- [Superset Docs](https://superset.apache.org/docs/)  
- [dbt Docs](https://docs.getdbt.com/)  
- [PostgreSQL Docs](https://www.postgresql.org/docs/)  
- [Docker](https://docs.docker.com/desktop/)  

---

For **detailed guides, troubleshooting, CI/CD, and security practices**, see [`README_SUMMARY.md`](README_SUMMARY.md).  
For **contributor workflow (branches, pulls, pushes)**, see [`GIT_WORKFLOW.md`](GIT_WORKFLOW.md).  

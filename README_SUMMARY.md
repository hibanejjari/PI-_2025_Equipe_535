# PI-_2025_Equipe_535

##  Overview
This project sets up a **data analytics pipeline** using:  
- **dbt** → transforms raw data into clean tables  
- **PostgreSQL** → stores raw + transformed data  
- **Python** → automation + anomaly detection  
- **Apache Superset** → dashboards & KPIs (read-only)  

**Workflow:**  
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
        │ - Enrichment  │       │   (read-only) │
        └───────────────┘       └───────────────┘
                 │
                 ▼
        (writes results back
           into PostgreSQL)


```

##  Table of Contents
1. [Overview](#-overview)
2. [Quickstart](#-quickstart)
   - [Start Superset (Docker)](#1-start-superset-docker)
   - [Install dbt (PostgreSQL)](#2-install-dbt-postgresql)
   - [Configure PostgreSQL Connection](#3-configure-postgresql-connection)
   - [Test + Run First Model](#4-test--run-first-model)
   - [Visualize in Superset](#5-visualize-in-superset)
3. [Key Files](#-key-files)
4. [References](#-references)

---

##  Quickstart

### 1. Start Superset (Docker)
```bash
git clone https://github.com/apache/superset.git
cd C:\Users\superset
docker compose -f docker-compose-non-dev.yml up -d
```
Open: [http://localhost:8088](http://localhost:8088)  
Login: `admin / admin`

---

### 2. Install dbt (PostgreSQL)
```bash
cd C:\Users\<YourName>\Documents
python -m venv dbt_env
C:\Users\<YourName>\Documents\dbt_env\Scripts\activate
pip install dbt-postgres
dbt init my_project
```

---

### 3. Configure PostgreSQL Connection
Create file: `C:\Users\<YourName>\.dbt\profiles.yml`  
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
cd C:\Users\<YourName>\Documents\my_project
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
Expected output: `1 | hello_dbt`

---

### 5. Visualize in Superset
- Go to **Superset → Data → Datasets → + Dataset**  
- Select your PostgreSQL DB  
- Create a chart → add it to a dashboard 🎉  

---

## Key Files
- `models/*.sql` → dbt transformations  
- `~/.dbt/profiles.yml` → PostgreSQL connection  
- `scripts/superset_check.py` → validate dashboards  
- `.gitlab-ci.yml` → CI/CD setup  

---

##  References
- [Superset Docs](https://superset.apache.org/docs/)  
- [dbt Docs](https://docs.getdbt.com/)  
- [PostgreSQL Docs](https://www.postgresql.org/docs/)  
- [Docker](https://docs.docker.com/desktop/)  

---

-> For detailed guides, troubleshooting, CI/CD, and security practices, see [`README_FULL.md`](README_FULL.md).

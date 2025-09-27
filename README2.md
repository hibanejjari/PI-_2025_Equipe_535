# PI-_2025_Equipe_535

This project sets up a complete analytics pipeline using **Apache Superset**, **PostgreSQL**, and **dbt**.  
The workflow is:  
```text
 Raw Data ──► dbt (Transformations) ──► PostgreSQL (Analytics Schema) ──► Superset (Dashboards & KPIs)
                                          │
                                          ▼
                             Python (Automation, Anomaly Detection, CI/CD)
```

## Table of Contents

### Setup
- [Setup & Prerequisites](#1-prerequisites)  
  Install required tools (Docker, Git, Python, WSL2) and verify they work.
  
(Summarized way to Set up)

- [Quickstart](#quickstart--superset--dbt--postgresql)  
  Run dbt → check PostgreSQL → load data in Superset → build a simple dashboard. 

(Detailed guide for setup)

- [Superset Setup](#2-get-and-run-superset-with-docker)  
  Run Apache Superset with Docker, access the UI, and confirm the service is up.

- [Setting up dbt with PostgreSQL](#setting-up-dbt-with-postgresql)  
  Create a dbt project, configure `profiles.yml`, and connect dbt to PostgreSQL.

---

### Code & Implementation
- [Working with the Real Database](#working-with-the-real-database)  
  Connect real raw tables, define sources, and write dbt transformation models.

- [Files to Modify or Add](#files-to-modify-or-add-once-real-database-is-connected)  
  List of key files to update (`models/src.yml`, `profiles.yml`, `superset_check.py`, `.gitlab-ci.yml`).

- [Python Integration](#python-integration)  
  Use Python scripts for anomaly detection, Superset API validation, and automation.

- [CI/CD Pipeline](#7-cicd-skeleton-gitlab)  
  Add automated checks using `pytest` and GitLab CI/CD.

---

### Informational
- [Troubleshooting](#8-troubleshooting)  
  Common errors (Docker not running, Superset auth failed) and fixes.

- [Security](#security)  
  Our practices for access control, database permissions, and encryption.

- [Diagrams](#diagrams)  
  Visual overview of the data pipeline and workflows.

- [Useful Links](#9-useful-links)  
  References to Superset docs, dbt docs, and GitHub repos.

# Summary of commands 
; details below if needed ( starting from the section **Apache Superset – Project 110 Guide (Windows**))

# Quickstart – Superset + dbt + PostgreSQL

---

## In 5 Minutes

1. **Start Superset (Docker)**
```bash
git clone https://github.com/apache/superset.git
cd C:\Users\superset
docker compose -f docker-compose-non-dev.yml up -d
```
Open: [http://localhost:8088](http://localhost:8088)  
Login: `admin / admin`

<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/01bb527d-335a-4cd0-9994-ec4e6cf04306" />

---

2. **Set up dbt**
```bash
cd C:\Users\<YourName>\Documents
python -m venv dbt_env
C:\Users\<YourName>\Documents\dbt_env\Scripts\activate
pip install dbt-postgres
dbt init my_project
```

<img width="848" height="136" alt="image" src="https://github.com/user-attachments/assets/392d5b04-34fd-4bec-81fa-cf503d79f65b" />

---

3. **Configure PostgreSQL connection**
Create `C:\Users\<YourName>\.dbt\profiles.yml`:
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

4. **Test connection**
```bash
cd C:\Users\<YourName>\Documents\my_project
dbt debug
```

<img width="1148" height="568" alt="image" src="https://github.com/user-attachments/assets/de6784a1-2396-42ab-b9ec-5d52affc6b83" />

---

5. **Run first model**
Create `models/hello_world.sql`:
```sql
SELECT 1 AS id, 'hello_dbt' AS message
```
Then run:
```bash
dbt run
```
Verify in PostgreSQL:
```sql
SELECT * FROM hello_world;
```

<img width="781" height="253" alt="image" src="https://github.com/user-attachments/assets/1ae6947a-8f55-48b2-9451-061be4444a10" />
<img width="636" height="333" alt="image" src="https://github.com/user-attachments/assets/17aab0fc-c137-4017-ba81-8624377bcb9b" />

---

If you see `1 | hello_dbt`, everything is working

---

After this, we will load **real raw data** into PostgreSQL, build transformations in **dbt**, and visualize them in **Superset dashboards**.

# Apache Superset – Project 110 Guide (Windows)

### 1) Prerequisites

- Windows 10/11 with admin rights  
- Docker Desktop installed and running (WSL2 backend enabled)  
- WSL2 (Windows Subsystem for Linux 2) installed and set as default  
- Git installed  
- Python 3.11 installed (Python 3.13 is also supported)  
- Chrome or Edge browser  

---

#### Verify Docker installation

```bash
docker version
```

```bash
docker run hello-world
```

Expected output includes Docker client and server versions, and a confirmation message from `hello-world`.

---

#### Verify WSL installation

```bash
wsl --version
```

```bash
wsl -l -v
```

```bash
wsl --set-default-version 2
```

Expected output should show your installed WSL version (2 recommended) and list Linux distributions.

---

#### Verify Python installation

```bash
python --version
```

Expected output:

```text
Python 3.11.x
```

```bash
where python
```

This shows the path where Python is installed.

---

#### Verify Git installation

```bash
git --version
```

Expected output:

```text
git version 2.x.x
```

---

### 2) Get and Run Superset with Docker

1. Make sure **Docker Desktop** is running.  
2. Open PowerShell and run:

```bash
cd C:\Users\
git clone https://github.com/apache/superset.git
cd C:\Users\superset
docker compose -f docker-compose-non-dev.yml pull
docker compose -f docker-compose-non-dev.yml up -d
```

Check services:

```bash
docker compose ps
docker compose logs -f
```

Open [http://localhost:8088](http://localhost:8088)

Default credentials:  
**Username:** `admin` / **Password:** `admin`

Then create 2 files:  
- `superset_check.py`  
- `reference_expected.csv`  

Run the Python script:  

```bash
python superset_check.py
```

---

### 3) Load Examples

```bash
docker compose exec superset_app superset load_examples
docker compose exec superset_app superset init
```

---

### 4) Add The First Dataset

1. In Superset UI → Data → Datasets → + Dataset  
2. Choose a database (like Postgres in the stack) or upload a CSV  
3. Create a chart and add it to a dashboard  

---

### 5) Superset API Basics

To put in your terminal

```http
POST /api/v1/security/login
GET  /api/v1/security/csrf_token
GET  /api/v1/dataset/{id}/data?format=json
POST /api/v1/chart/data
```

---

### 6) Python Proof of Concept – Validate Dashboard Data

```python
import requests, pandas as pd

BASE = "http://localhost:8088"
USER = "admin"
PWD = "admin"
DATASET_ID = 12
REFERENCE_CSV = "reference_expected.csv"

s = requests.Session()
r = s.post(
    f"{BASE}/api/v1/security/login",
    json={"provider":"db","username":USER,"password":PWD,"refresh":True},
    timeout=30,
)
r.raise_for_status()

s.headers.update({"Authorization": f"Bearer {r.json()['access_token']}"})

csrf = s.get(f"{BASE}/api/v1/security/csrf_token", timeout=30).json().get("result")
s.headers.update({"X-CSRFToken": csrf})

data = s.get(
    f"{BASE}/api/v1/dataset/{DATASET_ID}/data",
    params={"format":"json","row_limit":1000},
    timeout=60,
).json()
df_superset = pd.DataFrame(data)

df_ref = pd.read_csv(REFERENCE_CSV)

JOIN_KEYS = ["ds"]
VALUE_COL = "value"

merged = df_superset[JOIN_KEYS+[VALUE_COL]].merge(
    df_ref[JOIN_KEYS+[VALUE_COL]],
    on=JOIN_KEYS,
    how="outer",
    suffixes=("_superset","_ref")
)

merged["delta"] = merged[f"{VALUE_COL}_superset"] - merged[f"{VALUE_COL}_ref"]

merged["status"] = merged.apply(
    lambda r:
        "missing_in_ref" if pd.notna(r[f"{VALUE_COL}_superset"]) and pd.isna(r[f"{VALUE_COL}_ref"]) else
        ("missing_in_superset" if pd.isna(r[f"{VALUE_COL}_superset"]) and pd.notna(r[f"{VALUE_COL}_ref"]) else
         ("mismatch" if pd.notna(r["delta"]) and abs(r["delta"]) > 1e-9 else "match")),
    axis=1,
)

merged.to_csv("superset_vs_reference_report.csv", index=False)
print(merged["status"].value_counts())
```

Reference CSV template (`reference_expected.csv`): 

```csv
ds,value
2025-01-01,100
```

Run:

```bash
python superset_check.py
```

---

### 7) CI/CD Skeleton (GitLab)

**Test file: `test_validation.py`**

```python
import pandas as pd

def test_no_mismatches():
    df = pd.read_csv("superset_vs_reference_report.csv")
    assert not (df["status"] == "mismatch").any(), "Mismatches detected in dashboard data"
```

**Pipeline file: `.gitlab-ci.yml`**

```yaml
image: python:3.11-slim

before_script:
  - pip install requests pandas pytest python-dotenv

stages: [validate]

validate:
  stage: validate
  script:
    - python superset_check.py
    - pytest -q
```

---

### 8) Troubleshooting

1. **ConnectionRefusedError** → Superset not running:  

```bash
docker compose -f docker-compose-non-dev.yml up -d
```

2. **Pipe not found / cannot pull images** → Start Docker Desktop; enable WSL 2 backend:  

```bash
docker run hello-world
```

3. **Auth failed** → Update USER/PWD  
4. **Port 8088 in use** → Change mapping in `docker-compose-non-dev.yml`  

---

### 9) Useful Links

- API Overview: https://superset.apache.org/docs/api  
- GitHub Repo: https://github.com/apache/superset  

---

# Security

How we protect the data:

- **Secure Access & Authentication**: Role-based access control.  
- **Data Connections with Least Privilege**: Read-only accounts.  
- **Network & Encryption**: HTTPS, VPN/firewall protection.  

---

# Setting up dbt with PostgreSQL

## 1. Create a Python virtual environment
```bash
cd C:\Users\<YourName>\Documents
python -m venv dbt_env
```

## 2. Activate the environment
```bash
C:\Users\<YourName>\Documents\dbt_env\Scripts\activate
```

## 3. Install dbt for PostgreSQL
```bash
pip install dbt-postgres
dbt --version
```

## 4. Initialize a new dbt project
```bash
dbt init my_project
```

## 5. Configure the database connection
`C:\Users\<YourName>\.dbt\profiles.yml`

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

## 6. Test the connection
```bash
cd C:\Users\<YourName>\Documents\my_project
dbt debug
```

## 7. Create your first model
`models/hello_world.sql`

```sql
SELECT 1 AS id, 'hello_dbt' AS message
```

## 8. Run the model
```bash
dbt run
```

## 9. Verify in PostgreSQL
```sql
SELECT * FROM hello_world;
```

---

# Working with the real database

- Define raw tables in `src.yml`.  
- Write transformation models in `models/*.sql`.  
- Run transformations with `dbt run`.  
- Validate results in PostgreSQL.  
- Connect Superset to the transformed tables for dashboards.

---

# Files to Modify or Add Once Real Database Is Connected

- `my_project/models/src.yml`  
- `my_project/models/*.sql`  
- `~/.dbt/profiles.yml`  
- `scripts/superset_check.py`  
- `scripts/superset_fetch.py`  
- `tests/test_validation.py`  
- `./.gitlab-ci.yml`  

---

# ASCII Diagram

```text
Raw Data ──► dbt ──► PostgreSQL ──► Superset ──► Python (Automation/ML) ──► CI/CD
```

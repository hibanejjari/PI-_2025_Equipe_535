# PI-_2025_Equipe_535

This project sets up a complete analytics pipeline using **Apache Superset**, **PostgreSQL**, and **dbt**.  
The workflow is:  
```text
┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   Raw Data    │ ──► │      dbt      │ ──► │  PostgreSQL   │ ──► │   Superset    │ ──► │    Python     │
                │     │ - Transforms  │     │ - Stores raw  │     │ - Dashboards  │     │ - Automation  │
                │     │ - SQL models  │     │   & clean     │     │ - Charts & KPIs│    │ - Anomaly ML │
└───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘
```



## Table of Contents

### Setup
- [Setup & Prerequisites](#1-prerequisites)  
  Install required tools (Docker, Git, Python, WSL2) and verify they work.

-> **Simpler, Summarized Route**

- [Quickstart](#quickstart--superset--dbt--postgresql)  
  Run dbt → check PostgreSQL → load data in Superset → build a simple dashboard. 

-> **More Detailed Guides**

- [Superset Setup](#apache-superset--project-110-guide-windows) 
  Run Apache Superset with Docker, access the UI, and confirm the service is up.

- [Setting up dbt with PostgreSQL](#setting-up-dbt-with-postgresql)  
  Create a dbt project, configure `profiles.yml`, and connect dbt to PostgreSQL.


---

### Code & Implementation
- [Working with the Real Database](#working-with-the-real-database)  
  Connect real raw tables, define sources, and write dbt transformation models.

- [Files to Modify or Add](#files-to-modify-or-add-once-real-database-is-connected)  
  List of key files to update (`models/src.yml`, `profiles.yml`, `superset_check.py`, `.gitlab-ci.yml`).

- [Python Integration](#6-python-proof-of-concept--validate-dashboard-data)  
  Use Python scripts for anomaly detection, Superset API validation, and automation.

- [CI/CD Pipeline](#7-cicd-skeleton-gitlab)  
  Add automated checks using `pytest` and GitLab CI/CD.

---

### Informational
- [Troubleshooting](#8-troubleshooting)  
  Common errors (Docker not running, Superset auth failed) and fixes.

- [Security](#security)  
  Our practices for access control, database permissions, and encryption.

- [Diagrams](#ascii-diagram)  
  Visual overview of the data pipeline and workflows.
  
- [Useful Links](#9-useful-links)  
  References to Superset docs, dbt docs, GitHub repos, and installation guides / links for all required tools.

  
- [Project Structure](#project-structure)  
  Overview of how files and folders are organized in the repo.






# Summary of commands 
; details below if needed ( starting from the section **Apache Superset – Project 110 Guide (Windows**))
#  Quickstart – Superset + dbt + PostgreSQL


---

##  Fast route

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


#### Verify Git installation

```bash
git --version
```

Expected output:

```text
git version 2.x.x
```



### 2) Get and Run Superset with Docker

1. Make sure **Docker Desktop** is running.  
2. Open PowerShell and run:

```cd C:\Users\
git clone https://github.com/apache/superset.git
cd C:\Users\superset
docker compose -f docker-compose-non-dev.yml pull
docker compose -f docker-compose-non-dev.yml up -d
```

Check services:

```
docker compose ps
docker compose logs -f
```

Open ```[http://localhost:8088]```

Default credentials:  
**Username:** `admin` / **Password:** `admin`

Then create 2 files:  (that you can find on the github)
- `superset_check.py`  
- `reference_expected.csv`  

Run the Python script:   ( in the terminal of the folder in which you saved it)

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

( this is just an example of a dataset to test with)

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


## Once we have the right database (what to modify)

In Superset (one-time setup):  
- Add DB connection  
- Expose tables as Datasets  
- Check permissions  

In the script (`superset_fetch.py`):  

```python
import requests
import pandas as pd
import json

BASE = "https://your-superset.company.com/superset"   # TODO
USER = "your_user"                                    # TODO
PWD  = "your_password"                                # TODO
DATASET_ID = 0                                        # TODO

session = requests.Session()
login = session.post(
    f"{BASE}/api/v1/security/login",
    json={"username": USER, "password": PWD, "provider": "db", "refresh": True},
    timeout=30,
)
login.raise_for_status()
print("Logged in")

payload = {
    "datasource": {"id": DATASET_ID, "type": "table"},
    "queries": [{
        "columns": ["col1", "col2", "col3"],  # TODO
        "metrics": [],                        # TODO
        "filters": [],                        # TODO
        "orderby": [],
        "row_limit": 1000
    }],
    "result_format": "json",
    "result_type": "results",
}

data_resp = session.post(f"{BASE}/api/v1/chart/data", json=payload, timeout=60)
data_resp.raise_for_status()
```
superset.apache.org/docs/

### 9 Useful Links

**Superset Documentation**
- API Overview: https://superset.apache.org/docs/api  
- Installation Guide: https://superset.apache.org/docs/installation/installing-superset-using-docker-compose  
- Configuration Guide: https://superset.apache.org/docs/configuration/configuring-superset  

**dbt Documentation**
- dbt Core (Intro & Guides): https://docs.getdbt.com/docs/introduction  
- dbt Postgres Adapter: https://docs.getdbt.com/reference/warehouse-profiles/postgres-profile  
- dbt CLI Reference: https://docs.getdbt.com/reference/dbt-commands  

**PostgreSQL Documentation**
- Official Docs: https://www.postgresql.org/docs/  
- Windows Installer: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads  

**Docker**
- Install Docker Desktop (Windows/Mac): https://docs.docker.com/desktop/  
- Docker Compose Reference: https://docs.docker.com/compose/  

**Git**
- Git Installation: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git  

**Python**
- Python Downloads: https://www.python.org/downloads/  
- venv Documentation: https://docs.python.org/3/library/venv.html  


## Security

How we protect the data :

🔹 Secure Access & Authentication

We restrict access to Superset through user accounts and role-based permissions. Each user has credentials, and roles ensure that sensitive dashboards or datasets are only visible to authorized people. This prevents unauthorized access.
________________________________________
🔹 Data Connections with Least Privilege

Superset connects to databases using read-only accounts. This means users can query and visualize data but cannot modify or delete it. Access to the underlying data sources is minimized to reduce risks.
________________________________________
🔹 Network & Encryption

When deployed in production, Superset is placed behind a secure network (VPN or firewall) and served via HTTPS. This ensures that data in transit between the user’s browser and Superset is encrypted, protecting confidential information from interception

Test with SuperSet :

<img width="1060" height="464" alt="image" src="https://github.com/user-attachments/assets/9e57cba4-2a8b-49d9-907b-67cf51140189" />

## For the project, Superset is only the Frontend, we will also need

PostgreSQL → store data & anomaly results. ( Its SQL Shell terminal)

dbt → transformations + SQL modeling. (a developer framework for SQL inside the database.)

Python scripts (with scikit-learn / PyOD) → anomaly detection logic.

# Setting up dbt with PostgreSQL

-> setting up dbt with PostgreSQL, creating a project, and running first models.

---

## 1. Create a Python virtual environment
```bash
cd C:\Users\<YourName>\Documents
python -m venv dbt_env
```

---

## 2. Activate the environment
```bash
C:\Users\<YourName>\Documents\dbt_env\Scripts\activate
```
You should now see `(dbt_env)` at the start of your command line.

---

## 3. Install dbt for PostgreSQL
```bash
pip install dbt-postgres
dbt --version
```
If successful, you’ll see the installed dbt core and postgres adapter.

---

## 4. Initialize a new dbt project
```bash
dbt init my_project
```
This creates a folder `my_project/` with the starter configuration.

---

## 5. Configure the database connection
dbt needs a profile to connect to PostgreSQL.

1. Go to your home directory:
   ```bash
   C:\Users\<YourName>\.dbt\
   ```
2. Create a file called `profiles.yml` with this content:

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

⚠️ Replace `your_password_here` with your actual PostgreSQL password.

---

## 6. Test the connection
From inside your project folder:
```bash
cd C:\Users\<YourName>\Documents\my_project
dbt debug
```
If everything is correct, you should see **“All checks passed!”**

---

## 7. Create your first model
Inside `my_project/models/`, create a file called `hello_world.sql`:

```sql
SELECT 1 AS id, 'hello_dbt' AS message
```

---

## 8. Run the model
```bash
dbt run
```
dbt will build your model as a table/view inside PostgreSQL.  
You should see logs like:

```
1 of 1 OK created sql view model public.hello_world ... [CREATE VIEW in 0.18s]
Completed successfully
```

---

## 9. Verify in PostgreSQL
Open the `psql` shell and run:
```sql
SELECT * FROM hello_world;
```

Output:
```
 id |  message
----+-----------
  1 | hello_dbt
```

---

##  Working with the real database

Once a real database is available (instead of the simple `hello_world` model), the workflow is:

1. **Raw data**
   - Raw data = the original, unprocessed tables loaded into the database from source systems (sales, CRM, sensors, logs, etc.).
   - These tables often contain messy formats, inconsistent naming, duplicates, or missing values.
   - Example (raw table `orders_raw`):
     ```
     id | cust_id | amt | date_str
     1  |  101    |  50 | 2023-01-01
     2  |  101    |  30 | 01/02/2023
     3  |  102    | NULL| 2023-01-05
     ```

2. **Define sources**
   - In `models/`, create a `src.yml` file:
     ```yaml
     version: 2
     sources:
       - name: raw
         tables:
           - name: orders_raw
           - name: customers_raw
     ```

3. **Build transformation models**
   - Write SQL in `models/` to clean, join, or aggregate data.
   - Example `models/orders_clean.sql`:
     ```sql
     SELECT
         id,
         cust_id AS customer_id,
         COALESCE(amt, 0) AS amount,
         CAST(date_str AS DATE) AS order_date
     FROM {{ source('raw', 'orders_raw') }}
     ```

   - Clean result:
     ```
     id | customer_id | amount | order_date
     1  | 101         |   50   | 2023-01-01
     2  | 101         |   30   | 2023-01-02
     3  | 102         |    0   | 2023-01-05
     ```

4. **Run dbt**
   ```bash
   dbt run
   ```
   - dbt creates new tables/views (like `orders_clean`) inside your target schema.

5. **Use the results**
   - These dbt models can now be queried directly in PostgreSQL.
   - You can connect BI tools like **Superset** or **Power BI** to visualize the dbt-built tables.

---

With this workflow, dbt acts as the **transformation layer**:  
it takes raw data from your database, applies business logic, and creates clean, analytics-ready tables for dashboards and reports.

## ASCII Diagram 

```text
        ┌─────────────┐
        │   Raw Data  │   (sales, CRM, logs, sensors for example)
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │   dbt       │   (SQL transformations, cleaning, joins)
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │ PostgreSQL  │   (analytics schema with dbt models)
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │ Superset    │   (dashboards, KPIs, anomaly visualization)
        └─────────────┘
```



### Files to Modify or Add Once Real Database Is Connected

- `my_project/models/src.yml`  
  → define raw tables from the database  
  → **not auto-generated** (create manually after dbt init)  
  → **edit when new raw tables are added**  

- `my_project/models/*.sql`  
  → transformation models (cleaning, joining, standardizing)  
  → **folder auto-generated by dbt init**  
  → **create/edit SQL files frequently** (this is where most of the work happens)  

- `~/.dbt/profiles.yml`  
  → PostgreSQL connection details (host, user, password, schema)  
  → **not auto-generated** (must be created manually in home dir)  
  → **one-time setup**, rarely updated (only if credentials change)  

- `scripts/superset_check.py`  
  → validate Superset data vs reference CSV  
  → **not auto-generated** (create manually)  
  → **edit occasionally** (only if validation logic changes)  

- `scripts/superset_fetch.py`  
  → fetch results from Superset API  
  → **not auto-generated** (create manually)  
  → **edit occasionally** (to change dataset IDs or queries)  

- `tests/test_validation.py`  
  → automated data validation tests (pytest)  
  → **not auto-generated** (create manually)  
  → **edit often** when new tests are added  

- `./.gitlab-ci.yml`  
  → CI/CD pipeline config for dbt + Python checks  
  → **not auto-generated** (create manually at repo root)  
  → **edit occasionally** (when pipeline steps or dependencies change)  

  
                  ┌─────────────────────────┐
                  │   Raw Data (CRM, Logs,  │
                  │   Sensors, Sales) │
                  └─────────────┬───────────┘
                                │  (CSV/ETL)
                                ▼
                  ┌─────────────────────────┐
                  │ PostgreSQL Raw Tables   │
                  └─────────────┬───────────┘
                                │
                                ▼
                  ┌─────────────────────────┐
                  │ dbt (Transformations)   │
                  │  - models/*.sql         │
                  │  - src.yml              │
                  │  - profiles.yml         │
                  └─────────────┬───────────┘
                                │
                                ▼
                  ┌─────────────────────────┐
                  │ PostgreSQL Analytics    │
                  │ (Clean Tables / Views)  │
                  └─────────────┬───────────┘
                                │
                                ├─────────────────────► Superset
                                │                        - Datasets Config
                                │                        - Charts & KPIs
                                │                        - Dashboards
                                │
                                ▼
                  ┌─────────────────────────┐
                  │ Python Automation       │
                  │ - superset_check.py     │
                  │ - superset_fetch.py     │
                  │ - ML / PyOD Models      │
                  └─────────────┬───────────┘
                                │
                                ▼
                  ┌─────────────────────────┐
                  │ CI/CD (GitLab, pytest)  │
                  └─────────────┬───────────┘
                                │
                                ▼
                        End Users / Business Team


## Project Structure

├── analyses/ # Placeholder for dbt analyses (future reports or queries)

├── data/ # Raw/reference datasets

│ └── reference_expected.csv

├── dbt/ # dbt project configuration

│ └── dbt_project.yml

├── macros/ # Custom dbt macros (currently empty)

├── models/ # dbt models (SQL transformations)

│ ├── example/ # Example dbt models auto-generated

│ │ ├── my_first_dbt_model.sql

│ │ ├── my_second_dbt_model.sql

│ │ └── schema.yml

│ └── hello_world.sql # Custom model for initial dbt test

├── scripts/ # Python automation and validation scripts

│ └── superset_check.py

├── seeds/ # Static CSV seeds for dbt (empty placeholder)

├── snapshots/ # Snapshot definitions for dbt (empty placeholder)

├── tests/ # Unit tests and dbt schema tests

├── .gitignore

└── README.md

 Folder Roles
- **analyses/** → for dbt analysis files (SQL reports not meant as models).  
- **data/** → holds reference/test CSVs, like its used to validate Superset results.  
- **dbt/** → configuration for the dbt project (`dbt_project.yml`).  
- **macros/** → dbt macros (reusable SQL logic).  
- **models/** → main dbt transformations (`example/` = auto-generated, `hello_world.sql` = test model).  
- **scripts/** → Python scripts for automation, anomaly detection, or Superset validation.  
- **seeds/** → CSVs we want dbt to load as database tables.  
- **snapshots/** → to track slowly changing dimensions.  
- **tests/** → dbt or Python tests to validate the data models.  


This structure keeps **setup, transformations, scripts, and configuration** clearly separated for easier navigation.  









  
>>>>>>> a7d31d284143c9dee2fc9434f47adaf8f362d0a8

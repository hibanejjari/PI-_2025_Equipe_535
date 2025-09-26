# PI-_2025_Equipe_535

# Apache Superset – Project 110 Guide (Windows)

### 1)	Prerequisites

-	Windows 10/11 with admin rights

-	Docker Desktop installed and running (WSL 2 backend enabled)

-	Git installed

- Python 3.11 installed (ok if 3.13 is also present) 

- Chrome or Edge

Verify Docker:

In your main terminal after opening docker run : 
**docker version docker run hello-world**


**2)	Get and Run Superset with Docker**

Open PowerShell and run:

docker info

<img width="12" height="2" alt="image" src="https://github.com/user-attachments/assets/13914991-c531-4909-bc46-b932e559c4b1" />

```cd C:\Users\ git clone https://github.com/apache/superset.git ```

```cd C:\Users\\superset docker compose -f docker-compose-non-dev.yml```

```pull docker compose -f docker-compose-non-dev.yml up -d ```

Check services:

```docker compose ps```
```docker compose logs -f```

Open
```http://localhost:8088```

<img width="962" height="59" alt="image" src="https://github.com/user-attachments/assets/54e3a664-329f-46b2-bdb1-8b31581b101a" />

Default credentials: 

Username **admin** / Password **admin** (you can change them in the py file if you wish)

THEN create 2 files that you name **superset_check.py** (to edit based on the database given) and **reference_expected.csv**(find them on Teams files)	

**In short**

Start Docker + Superset (**docker compose -f docker-compose-non-dev.yml up -d**).

Create dataset + dashboard in Superset.

Save your expected results as reference_expected.csv in your project folder.

Run the Python script (python superset_check.py) from the same folder., 

**3)	Load Examples**

Run inside the app container: docker compose exec superset_app superset load_examples

Initialize (usually already done):
```docker compose exec superset_app superset init```

**4)	Add The First Dataset**

1	In Superset UI → Data → Datasets → + Dataset.
2	Choose a database (like Postgres in the stack) or upload a CSV.
3	Create a chart and add it to a dashboard.

**5)	Superset API Basics**

```POST /api/v1/security/login``` → get access token

```GET /api/v1/security/csrf_token``` → get CSRF token

```GET /api/v1/dataset/{id}/data?format=json``` → fetch rows

```POST /api/v1/chart/data``` → execute chart queries

Find your dataset id in the Explore URL (…?dataset=12…) (WE will have it once Vinci Energy gives it to us)


**6)	Python Proof of Concept – Validate Dashboard Data**

```import requests, pandas as pd

BASE = "http://localhost:8088"

USER = "admin"

PWD = "admin"

DATASET_ID = 12 # change to your dataset id 

REFERENCE_CSV = "reference_expected.csv" (Exemple to check if the code works)

s = requests.Session() r = s.post(f"{BASE}/api/v1/security/login", json={"provider":"db","username":USER,"password":PWD,"refresh":True}, timeout=30) r.raise_for_status()

s.headers.update({"Authorization": f"Bearer {r.json()['access_token']}"})

csrf = s.get(f"{BASE}/api/v1/security/csrf_token", timeout=30).json().get("result")

s.headers.update({"X-CSRFToken": csrf})

data = s.get(f"{BASE}/api/v1/dataset/{DATASET_ID}/data", params={"format":"json","row_limit":1000}, timeout=60).json() df_superset = pd.DataFrame(data)

df_ref = pd.read_csv(REFERENCE_CSV)

JOIN_KEYS = ["ds"] # change to your join keys VALUE_COL = "value" # change to your metric column

merged = df_superset[JOIN_KEYS+[VALUE_COL]].merge( df_ref[JOIN_KEYS+[VALUE_COL]], on=JOIN_KEYS, how="outer", suffixes=("_superset","_ref") ) merged["delta"] = merged[f"{VALUE_COL}_superset"] - merged[f"{VALUE_COL}_ref"] merged["status"] = merged.apply( lambda r: 

"missing_in_ref" if pd.notna(r[f"{VALUE_COL}_superset"]) and pd.isna(r[f"{VALUE_COL}_ref"]) else ("missing_in_superset" if pd.isna(r[f"{VALUE_COL}_superset"]) and pd.notna(r[f"{VALUE_COL}_ref"]) else ("mismatch" if pd.notna(r["delta"]) and abs(r["delta"])>1e-9 else "match")), axis=1)

merged.to_csv("superset_vs_reference_report.csv", index=False) print(merged["status"].value_counts())

Reference CSV template (reference_expected.csv):
ds,value 2025-01-01,100```

**Run the script:**
```python superset_check.py```
  	
**7)	CI/CD Skeleton (GitLab)**

**Test file** : ### test_validation.py 

import pandas as pd

def test_no_mismatches():

df = pd.read_csv("superset_vs_reference_report.csv")

assert not (df["status"] == "mismatch").any(), "Mismatches detected in dashboard data" Pipeline file:

### .gitlab-ci.yml image: python:3.11-slim

before_script: - pip install requests pandas pytest python-dotenv
stages: [validate]
validate:
stage: 
- validate script: - python superset_check.py
- pytest -q
  
**8)	Troubleshooting**
  
1	ConnectionRefusedError to localhost:8088 — Superset not running. Start: docker compose -f docker-compose-non-dev.yml up -d

2	Pipe not found / cannot pull images — Start Docker Desktop; enable WSL 2 backend; verify with docker run hello-world.

3	Auth failed — Update USER/PWD to your Superset admin credentials.

4	Port 8088 in use — Edit docker-compose-non-dev.yml and change host port (like 8090:8088).
  
**9)	Useful Links**

1	Superset Docs: https://superset.apache.org/docs/

2	API Overview: https://superset.apache.org/docs/api

3	GitHub Repo: https://github.com/apache/superset

# Once we have the right database : (what we need to modify)

In Superset (one-time setup)

Add the real DB connection: Settings → Data → Databases → + Database (provide SQLAlchemy URI, creds, SSL, etc.).

Expose your tables as Datasets: Data → Datasets → + Dataset (pick database, schema, table).

Permissions: ensure your user/role can read that database & datasets.

## In the script :

We need to update the variables **( fill out the TODO LINES)** ALL TO DO ON THE PYTHON FILE AND EXECUTE USING **python superset_fetch.py**


import requests

import pandas as pd

import json

# CONFIG (TODO: update later)

BASE = "https://your-superset.company.com/superset"   # TODO: your Superset URL (include /superset if needed)

USER = "your_user"                                     # TODO: your Superset username

PWD  = "your_password"                                 # TODO: your Superset password

DATASET_ID = 0                                         # TODO: put dataset id once dataset is created in Superset


# LOGIN

session = requests.Session()

login = session.post(

    f"{BASE}/api/v1/security/login",
    json={"username": USER, "password": PWD, "provider": "db", "refresh": True},
    timeout=30,
)

login.raise_for_status()

print("Logged in")


# QUERY (edit once you know real columns)

payload = {

    "datasource": {"id": DATASET_ID, "type": "table"},
    
    "queries": [{
    
        "columns": ["col1", "col2", "col3"],  # TODO: replace with real column names
        "metrics": [],                        # or add at least one metric if no columns
        "filters": [],                        # TODO: add filters if needed
        "orderby": [],
        "row_limit": 1000
    }],
    
    "result_format": "json",
    
    "result_type": "results",
}

data_resp = session.post(f"{BASE}/api/v1/chart/data", json=payload, timeout=60)

data_resp.raise_for_status()

rows = data_resp.json()["result"][0]["data"]

df_superset = pd.DataFrame(rows)

print("\n Sample data:\n", df_superset.head())


**How we protect the data :**

🔹 Secure Access & Authentication

We restrict access to Superset through user accounts and role-based permissions. Each user has credentials, and roles ensure that sensitive dashboards or datasets are only visible to authorized people. This prevents unauthorized access.
________________________________________

🔹 Data Connections with Least Privilege

Superset connects to databases using read-only accounts. This means users can query and visualize data but cannot modify or delete it. Access to the underlying data sources is minimized to reduce risks.
________________________________________

🔹 Network & Encryption

When deployed in production, Superset is placed behind a secure network (VPN or firewall) and served via HTTPS. This ensures that data in transit between the user’s browser and Superset is encrypted, protecting confidential information from interception



# PI-_2025_Equipe_535

# Apache Superset – Project 110 Guide (Windows)

### 1) Prerequisites

- Windows 10/11 with admin rights
- Docker Desktop installed and running (WSL 2 backend enabled)
- Git installed
- Python 3.11 installed (ok if 3.13 is also present)
- Chrome or Edge

Verify Docker:

```
docker version
docker run hello-world
```

---


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

### 9)	Useful Links

API Overview: https://superset.apache.org/docs/api

GitHub Repo: https://github.com/apache/superset


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



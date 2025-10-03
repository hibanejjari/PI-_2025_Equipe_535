# Notes


### 1. Configure WSL2 resources
Check your hardware in **Task Manager → Performance tab**: (ctrl + shift + esc)
- Under **CPU**, note cores and logical processors
- Under **Memory**, note installed RAM

Create a file in your Windows home directory:

`C:\Users\<YourUsername>\.wslconfig`

Example configuration (adjust based on your specs):

```ini
[wsl2]
memory=8GB
processors=6
swap=2GB
localhostForwarding=true
```

Apply the config by running in PowerShell:

```powershell
wsl --shutdown
```

Then restart Docker Desktop.

---

### 2. Start Superset

```powershell
git clone https://github.com/apache/superset.git
cd superset
```

From the project folder:

```powershell
docker compose -f docker-compose-non-dev.yml pull
docker compose -f docker-compose-non-dev.yml up -d --build

```

---

### 3. Verify containers
```powershell
docker compose ps
```
Ensure `superset_app` is **Started**.

---

### 4. Open in browser
```
http://localhost:8088
```
- Username: `admin`  
- Password: `admin`

---

### 5. First steps inside Superset
- Go to **Settings → Database Connections** to connect a datasource  
- Use **Datasets → +Dataset** to register a table or view  
- Create charts from datasets, then add them into a dashboard  

---

### 6. Stop Superset
```powershell
docker compose -f docker-compose-non-dev.yml down
```

---

## Explain

### 1. Upload CSV
Instead of PostgreSQL, we uploaded a **CSV** with columns:
(to do so you need to edit settings of database to allow import)
<img width="523" height="403" alt="image" src="https://github.com/user-attachments/assets/8b419800-eafc-408b-af41-fd878129efc3" />


# Progress Summary

- Set up Apache Superset locally with Docker Compose.  
- Created a test dashboard (ID 12) containing a **Table** and **Gantt** chart.  
- Wrote `ok.py` to:
  - Authenticate with Superset (`/api/v1/security/login`).
  - Fetch dashboard metadata (`/api/v1/dashboard/{id}`).
  - Extract chart IDs and names.
  - Query chart data (`/api/v1/chart/data`).
  - Run anomaly detection (z-score).
  - Output either detected anomalies or ` No anomalies found`.  
- Tested `ok.py` inside the virtual environment:
  - Successfully fetched 2 charts (`Table`, `Gantt`).
  - Retrieved 8 rows from each chart.
  - Verified anomaly detection works (no anomalies reported).  
- Cloned GitHub repo `PI-_2025_Equipe_535` and checked out branch **Hiba**.  
- Created `scripts/` folder inside repo, moved `ok.py` there.  
- Ran:
  - `git add scripts/ok.py`
  - `git commit -m "Add Superset anomaly validation script"`
  - `git push origin Hiba`  
- Confirmed script is now pushed to GitHub under `scripts/ok.py`.  

Current state: Superset + script fully working locally, code tracked on GitHub.

After cloning git, inside your git folder created in your folder : 

```
..\venv\Scripts\activate
```


Testing for anomalies with supersett and a csv filled with anamolies on purpose :

<img width="1464" height="615" alt="image" src="https://github.com/user-attachments/assets/3fbda885-9aa9-4912-9bb2-671130e1ac9d" />







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

- Superset running with dashboard ID 12 (which needs to be changed in the python code if its different, specified in the URL) created manually with 2 charts in it, by importing csv (Table + Gantt).  
- `scripts/ok.py`: logs in, fetches data, runs z-score anomaly check.  
- GitHub: branch Hiba, script pushed.  
- Test CSV confirmed anomaly detection works (`duration_days=50`, `cost=1200`).  
- Cloned GitHub repo `PI-_2025_Equipe_535` and checked out branch **Hiba**.  
- Created `scripts/` folder inside repo, moved `ok.py` there.  
 

After cloning git and installing requirements inside the cloned repo, inside your git folder created in your folder : 

```
pip install -r requirements.txt
```

From the project root (`PI-_2025_Equipe_535` folder):

```powershell
python -m venv ..\venv


..\venv\Scripts\activate
```


Testing for anomalies with supersett and a csv filled with anamolies on purpose :

<img width="1464" height="615" alt="image" src="https://github.com/user-attachments/assets/3fbda885-9aa9-4912-9bb2-671130e1ac9d" />


cloning and pushing to branch : 

<img width="1470" height="702" alt="image" src="https://github.com/user-attachments/assets/2e85276a-23e2-4fc8-9476-ea2f88e53cb8" />

<img width="1465" height="66" alt="image" src="https://github.com/user-attachments/assets/2e817414-3b4c-4ed3-b67f-a6d814e1270e" />


<img width="1473" height="674" alt="image" src="https://github.com/user-attachments/assets/6dcf81db-c5e3-4741-9244-b3b72d1d4602" />

### Git 

```powershell

git checkout Hiba                # your branch
git add scripts/ok.py test_data.csv
git commit -m "Add anomaly detection test with test_data.csv" # your comment
git pull origin Hiba            
git push origin Hiba

```         






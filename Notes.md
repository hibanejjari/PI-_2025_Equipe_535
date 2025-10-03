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

<img width="817" height="434" alt="image" src="https://github.com/user-attachments/assets/1b9e5f02-b3e7-4e16-84c4-e5cc5aa2008f" />




import requests
import json

SUPERSET_URL = "http://localhost:8088"
USERNAME = "admin"
PASSWORD = "admin"
DASHBOARD_ID = 12

# ---- Step 1: login and get token ----
login_url = f"{SUPERSET_URL}/api/v1/security/login"
payload = {
    "username": USERNAME,
    "password": PASSWORD,
    "provider": "db",
    "refresh": True
}
r = requests.post(login_url, json=payload)
r.raise_for_status()
access_token = r.json()["access_token"]
print("✅ Got access token")

headers = {"Authorization": f"Bearer {access_token}"}

# ---- Step 2: fetch dashboard metadata ----
dash_url = f"{SUPERSET_URL}/api/v1/dashboard/{DASHBOARD_ID}"
r_dash = requests.get(dash_url, headers=headers)
r_dash.raise_for_status()
dashboard = r_dash.json()["result"]

# parse position_json (it’s a JSON string, not dict)
pos_str = dashboard.get("position_json", "{}")
try:
    position = json.loads(pos_str)
except Exception as e:
    print("⚠️ Could not parse position_json:", e)
    position = {}

charts = []
for k, v in position.items():
    if isinstance(v, dict) and v.get("type") == "CHART":
        charts.append({
            "id": v["meta"]["chartId"],
            "name": v["meta"]["sliceName"]
        })

print(f"\n📊 Found {len(charts)} charts in dashboard {DASHBOARD_ID}:")
for c in charts:
    print("-", c["name"], f"(ID {c['id']})")
# ---- Step 3: fetch chart data + simple anomaly detection ----
import numpy as np

for c in charts:
    chart_id = c["id"]
    chart_url = f"{SUPERSET_URL}/api/v1/chart/{chart_id}"
    r_chart = requests.get(chart_url, headers=headers)
    r_chart.raise_for_status()
    chart_meta = r_chart.json()["result"]

    print(f"\n=== Chart Details: {c['name']} (ID {chart_id}) ===")
    print("Type:", chart_meta.get("viz_type"))
    print("Datasource:", chart_meta.get("datasource_name_text"))

    query_context = chart_meta.get("query_context")
    if not query_context:
        continue

    data_url = f"{SUPERSET_URL}/api/v1/chart/data"
    r_data = requests.post(data_url, headers=headers, json=json.loads(query_context))
    if r_data.status_code != 200:
        print(f"   ❌ Error fetching data: {r_data.status_code}")
        continue

    # ✅ Define data_json inside the loop
    data_json = r_data.json()
    rows = data_json.get("result", [])[0].get("data", [])
    print(f"   → Returned {len(rows)} rows")

    # --- anomaly detection (numeric columns) ---
    if rows and isinstance(rows[0], dict):
        anomalies_found = False
        for col in rows[0].keys():
            try:
                values = [float(r[col]) for r in rows if r[col] not in (None, "")]
                if not values:
                    continue
                mean, std = np.mean(values), np.std(values)
                anomalies = [
                    {"value": v, "zscore": (v - mean) / (std + 1e-9)}
                    for v in values if abs((v - mean) / (std + 1e-9)) > 2
                ]
                if anomalies:
                    anomalies_found = True
                    print(f"   ⚠️ Anomalies in column '{col}':")
                    for a in anomalies[:3]:  # show first 3 anomalies
                        print("      ", a)
            except (ValueError, TypeError):
                continue

        if not anomalies_found:
            print("   ✅ No anomalies found")

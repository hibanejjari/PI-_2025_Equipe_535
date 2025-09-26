import requests
import pandas as pd

# ------------------------------------------
# 🔧 Configuration (hardcoded for now)
# ------------------------------------------
BASE = "http://localhost:8088"   # Superset URL
USER = "admin"                   # Superset username
PWD = "admin"            # Superset password
DATASET_ID = 12                  # dataset ID
REFERENCE_CSV = "reference_expected.csv"  # ground truth file

# ------------------------------------------
# 1) Create a session and login
# ------------------------------------------
session = requests.Session()

login_resp = session.post(
    f"{BASE}/api/v1/security/login",
    json={
        "provider": "db",
        "username": USER,
        "password": PWD,
        "refresh": True
    },
    timeout=30,
)

if login_resp.status_code != 200:
    raise RuntimeError(f"Login failed: {login_resp.text}")

access_token = login_resp.json()["access_token"]
session.headers.update({"Authorization": f"Bearer {access_token}"})

# ------------------------------------------
# 2) Get CSRF token (needed for POST requests)
# ------------------------------------------
csrf_resp = session.get(f"{BASE}/api/v1/security/csrf_token", timeout=30)
csrf = csrf_resp.json().get("result") or csrf_resp.json().get("csrf_token")
session.headers.update({"X-CSRFToken": csrf})

# ------------------------------------------
# 3) Query dataset data
# ------------------------------------------
params = {"format": "json", "row_limit": 1000}
data_resp = session.get(f"{BASE}/api/v1/dataset/{DATASET_ID}/data", params=params, timeout=60)

if data_resp.status_code != 200:
    raise RuntimeError(f"Failed to fetch dataset: {data_resp.text}")

rows = data_resp.json()
df_superset = pd.DataFrame(rows)
print("\n✅ Superset sample:\n", df_superset.head())

# ------------------------------------------
# 4) Load reference data
# ------------------------------------------
df_ref = pd.read_csv(REFERENCE_CSV)
print("\n✅ Reference sample:\n", df_ref.head())

# ------------------------------------------
# 5) Compare values
#    (adjust join keys + column names to your dataset)
# ------------------------------------------
JOIN_KEYS = ["ds"]       # change to dataset’s key columns
VALUE_COL = "value"      # change to the metric column

# Check columns exist
for col in JOIN_KEYS + [VALUE_COL]:
    if col not in df_superset.columns:
        raise ValueError(f"Column {col} missing in Superset data")
    if col not in df_ref.columns:
        raise ValueError(f"Column {col} missing in reference data")

merged = df_superset[JOIN_KEYS + [VALUE_COL]].merge(
    df_ref[JOIN_KEYS + [VALUE_COL]],
    on=JOIN_KEYS,
    how="outer",
    suffixes=("_superset", "_ref")
)

merged["delta"] = merged[f"{VALUE_COL}_superset"] - merged[f"{VALUE_COL}_ref"]
merged["status"] = merged.apply(
    lambda r: (
        "missing_in_ref" if pd.notna(r[f"{VALUE_COL}_superset"]) and pd.isna(r[f"{VALUE_COL}_ref"]) else
        "missing_in_superset" if pd.isna(r[f"{VALUE_COL}_superset"]) and pd.notna(r[f"{VALUE_COL}_ref"]) else
        ("mismatch" if pd.notna(r["delta"]) and abs(r["delta"]) > 1e-9 else "match")
    ),
    axis=1
)

# ------------------------------------------
# 6) Save report
# ------------------------------------------
report_path = "superset_vs_reference_report.csv"
merged.to_csv(report_path, index=False)
print(f"\n📄 Report written to {report_path}")
print("\n📊 Summary:\n", merged["status"].value_counts())

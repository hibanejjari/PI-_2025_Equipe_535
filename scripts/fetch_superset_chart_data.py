import requests
import json
from pathlib import Path

# --- CONFIGURATION ---
SUPERSET_URL = "http://localhost:8088"  # Your Superset Base URL
USERNAME = "admin"
PASSWORD = "admin"
CHART_ID = 120

# 1. Get the directory where THIS script is located
# 2. .parent moves up to the project root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
# 3. Ensure the data folder exists (optional but recommended)
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR /f"chart_{CHART_ID}_data.json" # Name of the file to save

def fetch_and_save_data():
    session = requests.Session()

    # 1. AUTHENTICATION
    print(f"🔐 Authenticating as {USERNAME}...")
    login_url = f"{SUPERSET_URL}/api/v1/security/login"
    try:
        login_resp = session.post(login_url, json={
            "username": USERNAME,
            "password": PASSWORD,
            "provider": "db"
        })
        login_resp.raise_for_status()
        token = login_resp.json().get("access_token")
        session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
        print("✅ Authentication successful.")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return

    # 2. GET CHART METADATA
    print(f"📥 Fetching query context for Chart {CHART_ID}...")
    chart_url = f"{SUPERSET_URL}/api/v1/chart/{CHART_ID}"
    try:
        chart_resp = session.get(chart_url)
        chart_resp.raise_for_status()
        
        # Parse the stored query context
        raw_context = chart_resp.json().get("result", {}).get("query_context")
        if not raw_context:
            print("❌ No query context found. Please ensure the chart is saved.")
            return
            
        query_payload = json.loads(raw_context)
        
        # Ensure we get JSON back
        query_payload["result_format"] = "json"
        query_payload["result_type"] = "full"

    except Exception as e:
        print(f"❌ Failed to fetch chart metadata: {e}")
        return

    # 3. FETCH DATA
    print(f"🚀 Executing query...")
    data_url = f"{SUPERSET_URL}/api/v1/chart/data"
    try:
        data_resp = session.post(data_url, json=query_payload)
        data_resp.raise_for_status()
        
        # Extract just the data list from the response envelope
        result_envelope = data_resp.json()
        final_data = result_envelope['result'][0]['data']
        
        # 4. SAVE TO JSON FILE
        print(f"💾 Saving {len(final_data)} records to '{OUTPUT_FILE}'...")
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4)
            
        print("✅ Done! File saved successfully.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch data: {e}")
        print(f"Response: {data_resp.text}")

if __name__ == "__main__":
    fetch_and_save_data()
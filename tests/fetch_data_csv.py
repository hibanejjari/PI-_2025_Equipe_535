import requests
import json

# --- CONFIGURATION ---
SUPERSET_URL = "http://localhost:8088"
USERNAME = "admin"
PASSWORD = "admin"
CHART_ID = 102
OUTPUT_FILE = f"chart_{CHART_ID}_data.csv" # Change extension to .csv

def fetch_and_save_data():
    session = requests.Session()

    # 1. AUTHENTICATION (Same as before)
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
        
        raw_context = chart_resp.json().get("result", {}).get("query_context")
        if not raw_context:
            print("❌ No query context found.")
            return
            
        query_payload = json.loads(raw_context)
        
        # --- KEY CHANGE 1: Request CSV format ---
        query_payload["result_format"] = "csv"
        query_payload["result_type"] = "full"

    except Exception as e:
        print(f"❌ Failed to fetch chart metadata: {e}")
        return

    # 3. FETCH DATA
    print(f"🚀 Executing query (requesting CSV)...")
    data_url = f"{SUPERSET_URL}/api/v1/chart/data"
    try:
        data_resp = session.post(data_url, json=query_payload)
        data_resp.raise_for_status()
        
        # --- KEY CHANGE 2: Handle raw text instead of .json() ---
        # When result_format is 'csv', Superset returns the CSV data as the response body directly.
        csv_data = data_resp.text
        
        # 4. SAVE TO CSV FILE
        print(f"💾 Saving data to '{OUTPUT_FILE}'...")
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(csv_data)
            
        print("✅ Done! CSV file saved successfully.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch data: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
## Key functions

1. **Credential Exchange (Auth)**: The script starts by sending your admin credentials to the Superset Security API. It receives an access token, which acts as a digital key for all subsequent requests.

2. **Query Discovery**: Instead of guessing the SQL, the script queries the specific CHART_ID. It retrieves the Query Context—a JSON object that contains the exact filters, metrics, and dimensions used to build that chart.

3. **Format Override**: The script "intercepts" that query context and modifies it. It changes the result_format from the default JSON to CSV, ensuring the server returns a flat file rather than a complex web object.

4. **Remote Execution**: It sends the modified query back to the Superset /chart/data endpoint. The server executes the query against its underlying database and streams the results back as raw text.

5. **Path Resolution**: Using pathlib, the script determines the absolute path to your project's /data folder, ensuring the code works correctly regardless of which folder you run it from.

6. **Local Persistence**: Finally, it opens a file stream and writes the raw response directly to disk as a .csv file, effectively "syncing" the cloud chart data to your local environment.
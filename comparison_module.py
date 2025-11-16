import pandas as pd
import psycopg2
import json
from io import StringIO
from datetime import datetime

# --- Étape 1 : Simulation de la réponse de l'API Superset ---
superset_api_response = {
    "query": {
        "sql": """
          SELECT product_id, product_name, total_sales, date
          FROM sales;
        """,
        "results": [
            {"product_id": 101, "product_name": "Laptop", "total_sales": 12000, "date": "2025-11-01"},
            {"product_id": 102, "product_name": "Monitor", "total_sales": 3500, "date": "2025-11-01"},
            {"product_id": 103, "product_name": "Keyboard", "total_sales": 750, "date": "2025-11-02"},
            {"product_id": 104, "product_name": "Mouse", "total_sales": 400, "date": "2025-11-02"},
            {"product_id": 101, "product_name": "Laptop", "total_sales": 11500, "date": "2025-11-03"},
            {"product_id": 103, "product_name": "Keyboard", "total_sales": 800, "date": "2025-11-03"}
        ]
    }
}

# --- Étape 2 : Extraction des données Superset ---
superset_data = pd.DataFrame(superset_api_response["query"]["results"])
superset_sql = superset_api_response["query"]["sql"].strip()  # Requête SQL brute

# --- Étape 3 : Connexion à PostgreSQL et exécution de la requête ---
def execute_pg_query(sql_query, conn_params):
    """Exécute une requête SQL sur PostgreSQL et retourne un DataFrame."""
    conn = psycopg2.connect(**conn_params)
    df = pd.read_sql(sql_query, conn)
    conn.close()
    return df

# Paramètres de connexion (à adapter)
conn_params = {
    "dbname": "test_vinci_1",
    "user": "postgres",
    "password": "AurianeSQL",
    "host": "localhost"
}

# Exécution de la requête Superset sur PostgreSQL
reference_data = execute_pg_query(superset_sql, conn_params)

# --- Étape 4 : Comparaison automatique ---
def compare_dataframes(df1, df2, key_columns):
    """Compare deux DataFrames et retourne les écarts."""
    merged = df1.merge(
        df2,
        on=key_columns,
        suffixes=('_superset', '_reference'),
        how='outer',
        indicator=True
    )
    discrepancies = merged[merged['_merge'] != 'both']
    discrepancies = discrepancies[
        (discrepancies[f"total_sales_superset"] != discrepancies[f"total_sales_reference"]) |
        (discrepancies[f"product_name_superset"] != discrepancies[f"product_name_reference"])
    ]
    return discrepancies

# Détection des écarts
discrepancies = compare_dataframes(
    superset_data,
    reference_data,
    key_columns=["product_id", "date"]
)

# --- Étape 5 : Affichage des résultats ---
print("Données Superset :\n", superset_data)
print("\nDonnées PostgreSQL :\n", reference_data)
print("\nÉcarts détectés :\n", discrepancies[["product_id", "date", "total_sales_superset", "total_sales_reference"]])

# --- Étape 6 : Génération du rapport TXT ---
def generate_discrepancy_report(discrepancies, output_file="discrepancies_report.txt"):
    """Génère un fichier TXT avec le résumé des écarts."""
    with open(output_file, "w") as f:
        f.write("=== RAPPORT DE COMPARAISON SUPERSET vs POSTGRESQL ===\n")
        f.write(f"Date du rapport : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Nombre d'écarts détectés : {len(discrepancies)}\n\n")
        f.write("Détails des écarts :\n")
        f.write("--------------------------------------------------\n")
        for _, row in discrepancies.iterrows():
            f.write(
                f"ID Produit: {row['product_id']}, Date: {row['date']}\n"
                f"  - Superset: {row['total_sales_superset']} (vs PostgreSQL: {row['total_sales_reference']})\n"
                f"  - Écart: {abs(row['total_sales_superset'] - row['total_sales_reference'])}\n\n"
            )
        f.write("=== FIN DU RAPPORT ===")

# Génération du rapport
generate_discrepancy_report(discrepancies)
print(f"Rapport généré : discrepancies_report.txt")
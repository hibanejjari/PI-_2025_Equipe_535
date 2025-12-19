import pandas as pd
from clickhouse_connect import get_client

def importer_excel_vers_clickhouse(fichier_excel, host, username, password, base):
    client = get_client(host=host, username=username, password=password, database=base)

    xls = pd.ExcelFile(fichier_excel)
    writer = pd.ExcelWriter(fichier_excel, engine='openpyxl', mode='w')

    for feuille in xls.sheet_names:
        df = pd.read_excel(fichier_excel, sheet_name=feuille)

        if df.empty:
            continue

        table = feuille

        # Inférer types ClickHouse
        type_mapping = {
            'int64': 'Int64',
            'float64': 'Float64',
            'object': 'String',
            'datetime64[ns]': 'DateTime',
            'bool': 'Bool'
        }
        
        schema_cols = ", ".join([f"{col} {type_mapping[str(df[col].dtype)]}" for col in df.columns])

        # Créer table si inexistante
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {table} (
            {schema_cols}
        ) ENGINE = MergeTree() ORDER BY tuple();
        """
        client.command(create_sql)

        # Insérer données
        client.insert_df(table, df)

        # Vider la feuille Excel
        empty_df = df.iloc[0:0]
        empty_df.to_excel(writer, sheet_name=feuille, index=False)

    writer.close()
    print("Import terminé et Excel nettoyé.")

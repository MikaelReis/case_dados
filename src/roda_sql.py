import sqlite3
import pandas as pd

# Abre o banco
con = sqlite3.connect("output/allocacoes.db")

# Executa uma query
df = pd.read_sql_query("SELECT COUNT(*) AS total_registros FROM fato_playlist_alocacoes", con)
print(df)

con.close()

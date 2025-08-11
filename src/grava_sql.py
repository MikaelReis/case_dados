from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

DB_PATH = OUTPUT_DIR / "allocacoes.db"

# lê os CSVs 
produtos = pd.read_csv(DATA_DIR / "produtos.csv")
lojas = pd.read_csv(DATA_DIR / "lojas.csv")
vendas_7d = pd.read_csv(DATA_DIR / "vendas_7d.csv")
estoque_lojas = pd.read_csv(DATA_DIR / "estoque_lojas.csv")
estoque_cd = pd.read_csv(DATA_DIR / "estoque_cd.csv")


# Abre o Excel gerado pelo seu script principal
playlist_xlsx = OUTPUT_DIR / "playlist_alocacoes.xlsx"
playlist = pd.read_excel(playlist_xlsx, sheet_name="playlist")

# grava no SQLite
con = sqlite3.connect(DB_PATH)

# dimensões
produtos.to_sql("dim_produtos", con, if_exists="replace", index=False)
lojas.to_sql("dim_lojas", con, if_exists="replace", index=False)

# fatos de apoio
vendas_7d.to_sql("fato_vendas_7d", con, if_exists="replace", index=False)
estoque_lojas.to_sql("fato_estoque_lojas", con, if_exists="replace", index=False)
estoque_cd.to_sql("fato_estoque_cd", con, if_exists="replace", index=False)

# fato final: playlist
playlist.to_sql("fato_playlist_alocacoes", con, if_exists="replace", index=False)

# índices úteis (deixam consultas rápidas)
cur = con.cursor()
cur.executescript("""
CREATE INDEX IF NOT EXISTS idx_dim_produtos_id ON dim_produtos(id_produto);
CREATE INDEX IF NOT EXISTS idx_dim_lojas_id ON dim_lojas(id_loja);

CREATE INDEX IF NOT EXISTS idx_fv7d_prod_loja ON fato_vendas_7d(id_produto, id_loja);
CREATE INDEX IF NOT EXISTS idx_festoque_lojas_prod_loja ON fato_estoque_lojas(id_produto, id_loja);
CREATE INDEX IF NOT EXISTS idx_festoque_cd_prod ON fato_estoque_cd(id_produto);

CREATE INDEX IF NOT EXISTS idx_playlist_loja ON fato_playlist_alocacoes(id_loja);
CREATE INDEX IF NOT EXISTS idx_playlist_prod ON fato_playlist_alocacoes(id_produto);
CREATE INDEX IF NOT EXISTS idx_playlist_cat ON fato_playlist_alocacoes(categoria);
""")
con.commit()
con.close()

print("Banco gerado em:", DB_PATH)

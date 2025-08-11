from pathlib import Path    # lida com pastas/arquivos de forma segura
import pandas as pd         # manipulação de dados (tabelas)
import numpy as np          # operações numéricas (máximo, arredondamento etc.)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

BONUS_LANCAMENTO = 1.3      # +30% para lançamentos
ARREDONDAR_PARA_CIMA = True # arredondar para cima as recomendações
REPOSICAO_MINIMA = 0        # nunca recomendar negativo

produtos = pd.read_csv(DATA_DIR / "produtos.csv")
lojas = pd.read_csv(DATA_DIR / "lojas.csv")
vendas_7d = pd.read_csv(DATA_DIR / "vendas_7d.csv")
estoque_lojas = pd.read_csv(DATA_DIR / "estoque_lojas.csv")
estoque_cd = pd.read_csv(DATA_DIR / "estoque_cd.csv")

# junta vendas 7d
df = estoque_lojas.merge(vendas_7d, on=["id_produto", "id_loja"], how="left")

# junta atributos de produto (categoria, lançamento, etc.)
df = df.merge(produtos[["id_produto", "categoria", "preco", "lancamento"]], on="id_produto", how="left")

# junta atributos da loja (cluster, dias de cobertura)
df = df.merge(lojas[["id_loja", "cluster_loja", "dias_cobertura_meta"]], on="id_loja", how="left")

# junta estoque disponível no CD por produto
df = df.merge(estoque_cd, on="id_produto", how="left")

# demanda diária estimada = vendas dos últimos 7 dias / 7
df["demanda_diaria"] = df["vendido_7d"].fillna(0) / 7.0

# estoque alvo = demanda_diaria * dias_cobertura_meta
df["estoque_alvo"] = df["demanda_diaria"] * df["dias_cobertura_meta"]

# recomendação bruta = max(0, alvo - estoque atual)
df["recomendacao_bruta"] = (df["estoque_alvo"] - df["estoque_atual"]).clip(lower=REPOSICAO_MINIMA)

# se for lançamento, aplica bônus multiplicando a recomendação
df["recomendacao_ajustada"] = np.where(
    df["lancamento"], 
    df["recomendacao_bruta"] * BONUS_LANCAMENTO, 
    df["recomendacao_bruta"]
)

# arredondamento
if ARREDONDAR_PARA_CIMA:
    df["recomendacao_ajustada"] = np.ceil(df["recomendacao_ajustada"])
else:
    df["recomendacao_ajustada"] = np.round(df["recomendacao_ajustada"])

df["recomendacao_ajustada"] = df["recomendacao_ajustada"].astype(int)

# soma por produto
soma_por_produto = df.groupby("id_produto")["recomendacao_ajustada"].sum().rename("soma_recomendacao")
df = df.merge(soma_por_produto, on="id_produto", how="left")

# fator = min(1, estoque_CD / soma_recomendada)
df["fator_escala"] = np.minimum(
    1.0, 
    df["estoque_disponivel_cd"] / df["soma_recomendacao"].replace(0, np.nan)
)
df["fator_escala"] = df["fator_escala"].fillna(1.0)

# recomendação final escalada
df["recomendacao_final"] = np.floor(df["recomendacao_ajustada"] * df["fator_escala"]).astype(int)

# segurança: nada negativo
df["recomendacao_final"] = df["recomendacao_final"].clip(lower=0)


colunas_finais = [
    "id_loja", "id_produto", "categoria", "preco", "cluster_loja",
    "estoque_atual", "vendido_7d", "demanda_diaria", "dias_cobertura_meta",
    "estoque_alvo", "lancamento", "estoque_disponivel_cd", "recomendacao_final"
]

playlist = df[colunas_finais].sort_values(
    ["id_loja", "categoria", "recomendacao_final"], 
    ascending=[True, True, False]
)

# salva Excel
out_xlsx = OUTPUT_DIR / "playlist_alocacoes.xlsx"
with pd.ExcelWriter(out_xlsx, engine="xlsxwriter") as writer:
    playlist.to_excel(writer, sheet_name="playlist", index=False)

    ws = writer.sheets["playlist"]
    ws.set_column("A:A", 14)  # id_loja
    ws.set_column("B:B", 14)  # id_produto
    ws.set_column("C:C", 14)  # categoria
    ws.set_column("D:D", 10)  # preco
    ws.set_column("E:E", 12)  # cluster_loja
    ws.set_column("F:F", 14)  # estoque_atual
    ws.set_column("G:G", 12)  # vendido_7d
    ws.set_column("H:H", 14)  # demanda_diaria
    ws.set_column("I:I", 18)  # dias_cobertura_meta
    ws.set_column("J:J", 14)  # estoque_alvo
    ws.set_column("K:K", 12)  # lancamento
    ws.set_column("L:L", 20)  # estoque_disponivel_cd
    ws.set_column("M:M", 18)  # recomendacao_final

print("Arquivo gerado em:", out_xlsx)
print("Top 5 recomendações:")
print(playlist.nlargest(5, "recomendacao_final")[["id_loja", "id_produto", "recomendacao_final"]])





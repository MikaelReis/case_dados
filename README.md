# Case – Automação de Playlist de Produtos (Excel + Python + SQLite)

Projeto prático de **Planejamento & Alocação** (focado no dia a dia de lojas Nike/Fisia):
- Lê **CSV/Excel** com produtos, lojas, vendas 7d e estoques
- Calcula **demanda diária**, **estoque-alvo** e **recomendação de reposição**
- Aplica **bônus para lançamentos** e respeita **limite do CD**
- Gera **Excel** com playlist e grava **SQLite** para análises

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 1) Gerar playlist (output/playlist_alocacoes.xlsx)
python src/automacao_playlist.py

# 2) Gravar no SQLite (output/allocacoes.db)
python src/grava_sql.py

# 3) (Opcional) Teste rápido de SQL via Python
python src/roda_sql.py


Este projeto simula um cenário real de logística e reposição no varejo, automatizando todo o processo que normalmente seria feito manualmente em planilhas.
A partir dos dados de vendas, estoque e parâmetros de cobertura de cada loja, o sistema calcula de forma otimizada a quantidade ideal de reposição por produto, 
priorizando lançamentos e respeitando as restrições de estoque disponíveis no centro de distribuição.
Além disso, o resultado é exportado tanto em formato Excel, para fácil visualização e compartilhamento, quanto gravado em um banco de dados SQLite para permitir 
consultas e análises posteriores.

Este projeto foi construído explorando diferentes conceitos e ferramentas, realizando diversas consultas e ajustes para solucionar problemas encontrados durante
o desenvolvimento. Ele reflete meu interesse e perfil analítico, sempre buscando entender a performance dos processos e encontrar soluções eficientes. Estou em
constante evolução no universo da tecnologia e me aprofundando na área de dados, com foco em aplicar cada aprendizado em projetos práticos e desafiadores que
contribuam para meu crescimento profissional.

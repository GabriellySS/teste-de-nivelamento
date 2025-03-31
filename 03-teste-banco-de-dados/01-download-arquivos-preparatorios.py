"""
Código desenvolvido para extração de tabelas de um arquivo PDF, convertendo para um arquivo CSV e o compactando.
"""

# Importando as bibliotecas
import os
import pathlib
import requests

url_demonstracoes_contabeis = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis"
url_operadoras_plano_saude = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"

diretorio_projeto = os.path.abspath(os.path.join(pathlib.Path(__file__).parent.resolve(), ".."))
diretorio_downloads = os.path.join(diretorio_projeto, "downloads")
diretorio_demonstracoes_contabeis = os.path.join(diretorio_downloads, "demonstracoes-contabeis")
diretorio_operadoras_plano_saude = os.path.join(diretorio_downloads, "operadoras-plano-saude")
arquivo_operadoras_plano_saude = os.path.join(diretorio_operadoras_plano_saude, os.path.basename(url_operadoras_plano_saude))


print("Inicializando script para download dos arquivos preparatorios!")

# Criando o diretório para salvar os arquivos
os.makedirs(diretorio_demonstracoes_contabeis, exist_ok=True)
os.makedirs(diretorio_operadoras_plano_saude, exist_ok=True)

# Baixa os arquivos dos últimos 2 anos do repositório
def preparacao_demonstracao_contabeis():
    for ano in ["2023", "2024"]:
        pasta_ano = os.path.join(diretorio_demonstracoes_contabeis, ano)
        os.makedirs(pasta_ano, exist_ok=True)

        for trimestre in [1, 2, 3, 4]:
            nome_arquivo = f"{trimestre}T{ano}.zip"
            caminho_arquivo = os.path.join(pasta_ano, nome_arquivo)

            url_arquivo = f"{url_demonstracoes_contabeis}/{ano}/{nome_arquivo}"
            download_arquivo(url_arquivo, caminho_arquivo)

# Baixa os dados cadastrais das Operadoras Ativas na ANS no formato CSV
def preparacao_operadoras_plano_saude():
    download_arquivo(url_operadoras_plano_saude, arquivo_operadoras_plano_saude)

def download_arquivo(url_arquivo, caminho_arquivo):
    respostaArquivo = requests.get(url_arquivo, stream=True)
    if respostaArquivo.status_code == 200:
        with open(caminho_arquivo, "wb") as file:
            for chunk in respostaArquivo.iter_content(1024):
                file.write(chunk)
        print(f"Baixado: {caminho_arquivo}")


preparacao_demonstracao_contabeis()
preparacao_operadoras_plano_saude()

# def estruturar_tabelas():
#     conexao_banco = sqlite3.connect(arquivo_banco_de_dados)
#     cursor = conexao_banco.cursor()

#     df = pd.read_csv(arquivo_operadoras_plano_saude, sep=";")

#     df.columns = [col.strip().replace(" ", "_").replace("-", "_") for col in df.columns]

#     tipos_sqlite = {
#         "int64": "INTEGER",
#         "float64": "REAL",
#         "object": "TEXT",
#         "bool": "INTEGER",
#         "datetime64": "DATETIME"
#     }

#     nome_tabela = "operadoras_plano_saude"
#     colunas_sql = ", ".join([f"{col} {tipos_sqlite[str(df[col].dtype)]}" for col in df.columns])
#     sql_create = f"CREATE TABLE IF NOT EXISTS {nome_tabela} (id INTEGER PRIMARY KEY AUTOINCREMENT, {colunas_sql});"

#     cursor.execute(sql_create)
#     conexao_banco.commit()

#     df.to_sql(nome_tabela, conexao_banco, if_exists="append", index=False)
#     print(f"Dados inseridos na tabela '{nome_tabela}' com sucesso!")


# estruturar_tabelas()

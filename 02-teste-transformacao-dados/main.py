"""
Código desenvolvido para extração de tabelas de um arquivo PDF, convertendo para um arquivo CSV e o compactando.
"""

# Importando as bibliotecas
import os
import pathlib
from tabula import read_pdf
import pandas as pd
import zipfile

diretorio_projeto = os.path.abspath(os.path.join(pathlib.Path(__file__).parent.resolve(), ".."))
diretorio_downloads = os.path.join(diretorio_projeto, "downloads")

for arquivo in os.listdir(diretorio_downloads):
    if arquivo.startswith("Anexo_I_") and arquivo.endswith(".pdf"):

        print(f"Inicializando manipulação do arquivo {arquivo}")

        caminho_pdf = os.path.join(diretorio_downloads, arquivo)

        # Extraindo os dados da tabela
        tabelas = read_pdf(caminho_pdf, pages="all", lattice=True)

        # Unindo todas as tabelas
        unindo_tabelas = pd.concat(tabelas, ignore_index=True)

        # Removendo caracter de retorno das colunas
        unindo_tabelas.columns = [nome_coluna.replace("\r", " ") for nome_coluna in unindo_tabelas.columns]

        # Renomeando as colunas substituindo as abreviações
        unindo_tabelas = unindo_tabelas.rename(columns={
            "OD": "SEG. ODONTOLÓGICA", 
            "AMB": "SEG. AMBULATORIAL"
        })

        # Excluindo coluna Unnamed
        unindo_tabelas.drop(columns=["Unnamed: 0"], inplace=True)

        nome_arquivo_sem_extensao = arquivo.split('.pdf')[0]        
        arquivo_csv = f"{nome_arquivo_sem_extensao}.csv"
        caminho_csv = os.path.join(diretorio_downloads, arquivo_csv)

        # Salvando os dados em uma tabela estruturada em CSV
        unindo_tabelas.to_csv(caminho_csv, index=False)
        print(f"Arquivo CSV criado: {caminho_csv}")

        # Compactando o arquivo CSV em ZIP
        caminho_zip = os.path.join(diretorio_downloads, f"{arquivo_csv}.zip")

        with zipfile.ZipFile(caminho_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=5) as meu_zip:
            meu_zip.write(caminho_csv, arcname=os.path.basename(caminho_csv))

        print(f"Arquivo CSV compactado: {caminho_zip}")

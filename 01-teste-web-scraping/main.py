"""
Código desenvolvido para o download de determinados arquivos em pdf de um e compactação desses arquivos.
"""

# Importando as bibliotecas
import os
import pathlib
import requests
from bs4 import BeautifulSoup
import zipfile

# Declarando as variáveis
url_pagina = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
diretorio_projeto = os.path.abspath(os.path.join(pathlib.Path(__file__).parent.resolve(), ".."))
diretorio_downloads = os.path.join(diretorio_projeto, "downloads")

# Criando o diretório para salvar os arquivos
os.makedirs(diretorio_downloads, exist_ok=True)

resposta = requests.get(url_pagina)
soup = BeautifulSoup(resposta.text, "html.parser")

# Função para realizar o download de arquivos.
def download_arquivo(url_arquivo, caminho_arquivo):
    respostaArquivo = requests.get(url_arquivo, stream=True)
    if respostaArquivo.status_code == 200:
        with open(caminho_arquivo, "wb") as file:
            for chunk in respostaArquivo.iter_content(1024):
                file.write(chunk)
        print(f"Baixado: {caminho_arquivo}")

# Encontrando os links dos arquivos PDFs
for link in soup.find_all("a", href=True):
    if link.text == "Anexo I.":
        print("Achei o primeiro PDF. Anexo I.")
        url_arquivo = link["href"]
        nome_arquivo = url_arquivo.split("/")[-1]

        print(f"URL arquivo: {url_arquivo}")
        print(f"Nome arquivo: {nome_arquivo}")

        caminho_arquivo = os.path.join(diretorio_downloads, nome_arquivo)
        download_arquivo(url_arquivo, caminho_arquivo)

    if link.text == "Anexo II.":
        print("Achei o segundo PDF. Anexo II.")
        url_arquivo = link["href"]
        nome_arquivo = url_arquivo.split("/")[-1]

        print(f"URL arquivo: {url_arquivo}")
        print(f"Nome arquivo: {nome_arquivo}")

        caminho_arquivo = os.path.join(diretorio_downloads, nome_arquivo)
        download_arquivo(url_arquivo, caminho_arquivo)

        break

# Criando arquivo zip com os PDFs
anexos_zip = os.path.join(diretorio_downloads, "anexos")
anexos_zip = f"{anexos_zip}.zip"

with zipfile.ZipFile(anexos_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=5) as meu_zip:
    for arquivo in os.listdir(diretorio_downloads):
        if arquivo.endswith(".pdf"):
            caminho_pdf = os.path.join(diretorio_downloads, arquivo)
            meu_zip.write(caminho_pdf, arcname=arquivo)

    print(f"Arquivos PDFs compactados: {anexos_zip}")

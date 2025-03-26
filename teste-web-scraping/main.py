"""
Código desenvolvido para o download de determinados arquivos em pdf de um e compactação desses arquivos.
"""

# Importando as bibliotecas
import os
import sys
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import shutil

# Declarando as variáveis
urlPagina = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
resposta = requests.get(urlPagina)
soup = BeautifulSoup(resposta.text, "html.parser")

# Criando o diretório para salvar os arquivos
os.makedirs("downloads", exist_ok=True)

# Listagem dos arquivos a serem baixados
arquivosDesejados = {"Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf", "Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"}

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
    # print(dir(link))
    # print(link.text)

    if link.text == "Anexo I.":
        print("Achei o primeiro PDF. Anexo I.")
        url_arquivo = link["href"]
        nome_arquivo = url_arquivo.split("/")[-1]

        print(f"URL arquivo: {url_arquivo}")
        print(f"Nome arquivo: {nome_arquivo}")

        caminho_arquivo = os.path.join("downloads", nome_arquivo)
        download_arquivo(url_arquivo, caminho_arquivo)

    if link.text == "Anexo II.":
        print("Achei o segundo PDF. Anexo II.")
        url_arquivo = link["href"]
        nome_arquivo = url_arquivo.split("/")[-1]

        print(f"URL arquivo: {url_arquivo}")
        print(f"Nome arquivo: {nome_arquivo}")

        caminho_arquivo = os.path.join("downloads", nome_arquivo)
        download_arquivo(url_arquivo, caminho_arquivo)

        break

# Compactando a pasta downloads
shutil.make_archive("downloads", "zip", "downloads")
print("Pasta compactada com sucesso!")

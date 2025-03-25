"""
Código desenvolvido para o download de determinados arquivos em pdf de um e compactação desses arquivos.
"""

# Importando as bibliotecas
import os
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

# Encontrando os links dos arquivos pdf's
for link in soup.find_all("a", href=True):
    urlArquivo = link["href"]
    if urlArquivo == "#" or urlArquivo.strip() == "":
        continue
    if not urlArquivo.startswith("http"):
        urlArquivo = urljoin(urlPagina, urlArquivo)
    nomeArquivo = urlArquivo.split("/")[-1]
    if nomeArquivo in arquivosDesejados:
        urlArquivo = urljoin(urlPagina, urlArquivo)
        diretorioArquivo = os.path.join("downloads", nomeArquivo)

# Fazendo o download dos arquivos
respostaArquivo = requests.get(urlArquivo, stream=True)
if respostaArquivo.status_code == 200:
    with open(diretorioArquivo, "wb") as file:
        for chunk in respostaArquivo.iter_content(1024):
            file.write(chunk)
    print(f"Baixado: {diretorioArquivo}")

# Compactando a pasta downloads
shutil.make_archive("downloads", "zip", "downloads")
print("Pasta compactada com sucesso!")

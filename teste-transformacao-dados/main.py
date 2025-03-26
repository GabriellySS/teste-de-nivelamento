from tabula import read_pdf
import pandas as pd
import shutil


caminho_pdf = "arquivos/Anexo_I_Rol_2021RN_465.2021_RN627L_2024.pdf"

# Extraindo os dados da tabela
tabelas = read_pdf(caminho_pdf, pages="all", lattice=True)
print(f"Dados do PDF extraídos: {tabelas}")

# Unindo todas as tabelas
unindo_tabelas = pd.concat(tabelas, ignore_index=True)

# Renomeando as colunas substituindo as abreviações
unindo_tabelas = unindo_tabelas.rename(columns={
    "OD": "SEG. ODONTOLÓGICA", 
    "AMB": "SEG. AMBULATORIAL"
})

# Excluindo coluna Unnamed
unindo_tabelas.drop(columns=["Unnamed: 0"], inplace=True)

# Salvando os dados em uma tabela estruturada em CSV
caminho_csv = "arquivos/Anexo_I_Rol_2021RN_465.2021_RN627L_2024.csv"

unindo_tabelas.to_csv(caminho_csv, index=False)
print(f"Arquivo CSV criado: {unindo_tabelas}")

# Compactando o arquivo CSV em ZIP
caminho_zip = "arquivos/Anexo_I_Rol_2021RN_465.2021_RN627L_2024.zip"

shutil.make_archive(caminho_zip.replace(".zip", ""), "zip", ".", caminho_csv)
print(f"Arquivo CSV compactado: {caminho_zip}")

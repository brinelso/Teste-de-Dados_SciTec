import streamlit as st
import pygsheets
import pandas as pd
from dashboard import mostrar_dashboard
from forms import mostrar_formulario

st.set_page_config(
    page_title = 'Dashboard de Base Criminal',
    layout = 'wide'
)

st.sidebar.title('Navegação')
pagina = st.sidebar.radio(
    'Selecione uma Página',
    options = ['Dashboard', 'Adicionar Dados']
)

st.sidebar.divider()

if pagina == 'Dashboard':
    mostrar_dashboard()
else:
    mostrar_formulario()

# Conectando o bot, que tem acesso a planilha, com o projeto
chave_de_acesso= pygsheets.authorize(service_file="chave_de_acesso.json")
arquivo_GoogleSheets = "https://docs.google.com/spreadsheets/d/136DaNqFF7CKgLz1YM1nI-eB1v1Uf3rEdyvN6IJ36yTo/"
arquivo = chave_de_acesso.open_by_url(arquivo_GoogleSheets)
planilha = arquivo.worksheet_by_title("crime_rate_safety_analysis")
data = planilha.get_all_values()

# Criando o data frame
df = pd.DataFrame(data) # A partir de agora, pode usar o data frame normalmente, como se ele estivesse baixado no pc ou viesse de um .csv

# Teste de texto
st.title("Projeto final - Home")
st.write("Uma amostra de texto")

# Teste de conexão e escrita com a tabela
st.write(df)
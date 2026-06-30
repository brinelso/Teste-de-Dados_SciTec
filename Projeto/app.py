import streamlit as st
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
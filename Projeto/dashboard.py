import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashbord de Base Criminal",
    layout="wide"
)

CAMINHO_CSV = "crime_rate_safety_analysis.csv"

@st.cache_data
def carregar_dados(caminho):
    df = pd.read_csv(caminho)
    return df

df = carregar_dados(CAMINHO_CSV)

st.sidebar.header("Filtros")

paises_disponiveis = sorted(df['country'].dropna().unique())
paises_selecionados = st.sidebar.multiselect(
    "País",
    options=paises_disponiveis,
    default=paises_disponiveis
)

crimes_disponiveis = sorted(df['crime_type'].dropna().unique())
crimes_selecionados = st.sidebar.multiselect(
    "Tipo de Crime",
    options=crimes_disponiveis,
    default=crimes_disponiveis
)

ano_min = int(df['year'].min())
ano_max = int(df['year'].max())
intervalo_anos = st.sidebar.slider(
    "Ano",
    min_value=ano_min,
    max_value=ano_max,
    value=(ano_min, ano_max)
)

df_filtrado = df[
    (df['country'].isin(paises_selecionados)) &
    (df['crime_type'].isin(crimes_selecionados)) &
    (df['year'] >= intervalo_anos[0]) &
    (df['year'] <= intervalo_anos[1])
]
 
st.sidebar.markdown(f"**Registros filtrados:** {len(df_filtrado)}")

st.title("Dashboard da Base Criminal")
st.markdown("Use os filtros na barra lateral para explorar os dados.")

col1, col2 = st.columns(2)

with col1:
    top_cities = (
        df_filtrado['country']
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_cities.columns = ['País', 'Ocorrencias']
 
    cores = {
        'Brazil': '#009C3B',
        'Argentina': '#75AADB',
        'Germany': '#000000',
        'France': '#0055A4',
        'USA': '#B22234',
        'Mexico': '#006847',
        'India': '#FF9933',
        'Pakistan': '#01411C',
        'Turkey': '#E30A17',
        'Canada': '#FF0000'
    }
 
    fig1 = px.bar(
        top_cities,
        x='País',
        y='Ocorrencias',
        color='País',
        color_discrete_map=cores,
        title='Top 10 países com mais ocorrências'
    )
    fig1.update_layout(
        template='plotly_dark',
        title_x=0.5,
        showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    crime_count = (
        df_filtrado['crime_type']
        .value_counts()
        .reset_index()
    )
    crime_count.columns = ['Crime', 'Quantidade']
 
    fig2 = px.bar(
        crime_count,
        x='Crime',
        y='Quantidade',
        text='Quantidade',
        color='Quantidade',
        title='Quantidade de ocorrências por tipo de crime'
    )
    fig2.update_layout(
        template='plotly_dark',
        title_x=0.5,
        xaxis_title='Tipo de Crime',
        yaxis_title='Quantidade'
    )
    st.plotly_chart(fig2, use_container_width=True)

crime_year = (
    df_filtrado.groupby('year')
    .size()
    .reset_index(name='Quantidade')
)
 
fig3 = px.line(
    crime_year,
    x='year',
    y='Quantidade',
    markers=True,
    title='Ocorrências ao longo dos anos',
    color_discrete_sequence=["#b4291f"]
)
fig3.update_xaxes(tickmode='linear', dtick=1)
fig3.update_traces(line=dict(width=4), marker=dict(size=10))
fig3.update_layout(
    template='plotly_dark',
    title_x=0.5,
    xaxis_title='Ano',
    yaxis_title='Quantidade de Ocorrências'
)
st.plotly_chart(fig3, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig4 = px.box(
        df_filtrado,
        x='crime_type',
        y='crime_severity_score',
        title='Severidade por tipo de crime'
    )
    fig4.update_layout(
        template='plotly_dark',
        title_x=0.5,
        xaxis_title='Tipo de Crime',
        yaxis_title='Severidade do Crime'
    )
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    resolved = (
        df_filtrado['crime_resolved']
        .value_counts()
        .reset_index()
    )
    resolved.columns = ['Status', 'Quantidade']
 
    fig5 = px.pie(
        resolved,
        names='Status',
        values='Quantidade',
        title='Percentual de Crimes Resolvidos',
        color='Status',
        color_discrete_map={
            'Yes': '#2ecc71',
            'No': '#e74c3c'
        }
    )
    fig5.update_traces(textinfo='percent+label', textfont_size=18)
    fig5.update_layout(
        template='plotly_dark',
        title_x=0.5,
        title_font_size=24,
        font_size=16,
        legend_font_size=20
    )
    st.plotly_chart(fig5, use_container_width=True)